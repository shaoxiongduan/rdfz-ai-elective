import pygame
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from glob import glob
import os
from tqdm import tqdm

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20  # Changed to match the dataset size
CELL_SIZE = WIDTH // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (220, 179, 92)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Go - Five in a Row")

# Initialize the board
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Current player (True for black, False for white)
current_player = True

# Game state
MAIN_MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MAIN_MENU

# Font
font = pygame.font.Font(None, 36)

# Dataset paths
DATASET_PATH = 'dataset/gomocup2019results'  # Update this path

# Custom Dataset class
class GoDataset(Dataset):
    def __init__(self, dataset_path):
        self.file_list = glob(os.path.join(dataset_path, '*.npz'))
        self.data = []
        self.labels = []
        self.load_data()

    def load_data(self):
        for file_path in self.file_list:
            data = np.load(file_path)
            inputs = data['inputs']
            outputs = data['outputs']
            for input, output in zip(inputs, outputs):
                self.data.append(input)
                self.labels.append(np.argmax(output))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        input_tensor = torch.tensor(self.data[idx], dtype=torch.float32).unsqueeze(0)
        return input_tensor, torch.tensor(self.labels[idx], dtype=torch.long)

# Load dataset
dataset = GoDataset(DATASET_PATH)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)

# Define the CNN model
class GoNet(nn.Module):
    def __init__(self, input_channels, grid_size):
        super(GoNet, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * grid_size * grid_size, grid_size * grid_size)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

# Get input shape from the first item in the dataset
sample_input, _ = dataset[0]
input_channels, grid_size, _ = sample_input.shape

# Initialize the model, loss function, and optimizer
model = GoNet(input_channels, grid_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")
model.to(device)

# Load model from path if specified
model_path = 'checkpoints_completed/checkpoint_17000.pth'  # Update this path if needed
skip_training = True  # Set this to True to skip training and use the loaded model

if skip_training:
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    model.eval()
    print(f"Model loaded from {model_path}")
else:
    # Training loop
    num_epochs = 1
    checkpoint_interval = 1000  # Save checkpoint every 1000 steps
    checkpoint_dir = 'checkpoints'  # Directory to save checkpoints
    os.makedirs(checkpoint_dir, exist_ok=True)
    step = 0

    print("Starting model training...")
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for i, (inputs, labels) in enumerate(tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            step += 1

            if step % checkpoint_interval == 0:
                checkpoint_path = os.path.join(checkpoint_dir, f'checkpoint_{step}.pth')
                torch.save(model.state_dict(), checkpoint_path)
                print(f"Checkpoint saved at step {step} in {checkpoint_path}")

            if (i + 1) % 10 == 0:
                print(f"Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}")
        
        print(f"Epoch [{epoch+1}/{num_epochs}] completed. Average Loss: {total_loss/len(train_loader):.4f}")

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
        print(f"Validation Loss: {val_loss/len(val_loader):.4f}")

    print("Model training completed.")
    torch.save(model.state_dict(), 'go_model.pth')

def draw_board():
    screen.fill(BOARD_COLOR)
    for x in range(GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[y][x] is not None:
                color = BLACK if board[y][x] else WHITE
                center = (x * CELL_SIZE, y * CELL_SIZE)
                pygame.draw.circle(screen, color, center, CELL_SIZE // 2 - 2)

    # Display current player's turn
    turn_text = font.render(f"{'Black' if current_player else 'White'}'s Turn", True, BLACK)
    screen.blit(turn_text, (10, 10))

def check_win(x, y):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + i*dx, y + i*dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] == board[y][x]:
                count += 1
            else:
                break
        for i in range(1, 5):
            nx, ny = x - i*dx, y - i*dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] == board[y][x]:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h))

    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

def start_pvp_game():
    global game_state, board, current_player, ai_enabled
    game_state = PLAYING
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = True
    ai_enabled = False

def start_ai_game():
    global game_state, board, current_player, ai_model, ai_enabled
    game_state = PLAYING
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = True
    ai_model = model
    ai_model.to(device)
    ai_enabled = True

def draw_main_menu():
    screen.fill(BOARD_COLOR)
    draw_button("Play with Person", 200, 200, 200, 50, start_pvp_game)
    draw_button("Play with AI", 200, 300, 200, 50, start_ai_game)

def draw_game_over(winner):
    screen.fill(BOARD_COLOR)
    game_over_text = font.render(f"{winner} wins!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    draw_button("Main Menu", 200, 400, 200, 50, lambda: set_game_state(MAIN_MENU))

def set_game_state(state):
    global game_state, board, current_player
    print(game_state)
    game_state = state
    if state == MAIN_MENU:
        board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        current_player = True

def ai_move():
    global board, current_player, game_state, winner
    input_tensor = torch.zeros((1, 1, GRID_SIZE, GRID_SIZE))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] is True:
                input_tensor[0, 0, y, x] = 1
            elif board[y][x] is False:
                input_tensor[0, 0, y, x] = -1
    
    with torch.no_grad():
        output = ai_model(input_tensor.to(device))
    
    move = output.argmax().item()
    x, y = move % GRID_SIZE, move // GRID_SIZE
    
    while board[y][x] is not None:
        output[0, move] = float('-inf')
        move = output.argmax().item()
        x, y = move % GRID_SIZE, move // GRID_SIZE
    
    board[y][x] = current_player
    if check_win(x, y):
        winner = "Black" if current_player else "White"
        game_state = GAME_OVER
    current_player = not current_player

# Main game loop
running = True
ai_enabled = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == PLAYING:
            x, y = event.pos
            grid_x = round(x / CELL_SIZE)
            grid_y = round(y / CELL_SIZE)
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and board[grid_y][grid_x] is None:
                board[grid_y][grid_x] = current_player
                if check_win(grid_x, grid_y):
                    winner = "Black" if current_player else "White"
                    game_state = GAME_OVER
                current_player = not current_player

                # AI move
                if game_state == PLAYING and not current_player and ai_enabled:
                    ai_move()

    if game_state == MAIN_MENU:
        draw_main_menu()
    elif game_state == PLAYING:
        draw_board()
    elif game_state == GAME_OVER:
        draw_game_over(winner)

    pygame.display.flip()

pygame.quit()
sys.exit()

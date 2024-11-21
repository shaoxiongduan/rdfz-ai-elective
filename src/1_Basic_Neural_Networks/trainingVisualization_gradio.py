import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
import gradio as gr
import matplotlib.animation as animation

# Function to generate data
def generate_data(data_type='quadratic'):
    np.random.seed(np.random.randint(0, 1000))
    x = np.random.uniform(-10, 10, 100)
    if data_type == 'quadratic':
        y = 3 * x**2 + 2 * x + 1 + np.random.normal(0, 10, 100)
    elif data_type == 'linear':
        y = 2 * x + 1 + np.random.normal(0, 5, 100)
    elif data_type == 'sinusoidal':
        y = 10 * np.sin(x) + np.random.normal(0, 2, 100)
    elif data_type == 'exponential':
        y = np.exp(0.5 * x) + np.random.normal(0, 2, 100)
    else:  # random
        y = np.random.normal(0, 20, 100)
    return x, y

# Initial data generation
x, y = generate_data()

# Split into train and validation sets
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.1, random_state=0)

# Define the neural network
class SimpleNN(nn.Module):
    def __init__(self, hidden_dims):
        super(SimpleNN, self).__init__()
        layers = []
        input_dim = 1
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(input_dim, int(hidden_dim)))
            layers.append(nn.ReLU())
            input_dim = int(hidden_dim)
        layers.append(nn.Linear(input_dim, 1))
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)

def visualize_network(model, x_train, y_train, x_val, y_val, train_loss_history, val_loss_history, epochs):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    
    # Plot network output
    ax1.scatter(x_train, y_train, color='blue', label='Train set')
    ax1.scatter(x_val, y_val, color='red', label='Validation set')
    
    # Generate predictions
    x_range = np.linspace(-10, 10, 1000).reshape(-1, 1)
    x_range_tensor = torch.tensor(x_range, dtype=torch.float32)
    y_pred = model(x_range_tensor).detach().numpy()
    
    ax1.plot(x_range, y_pred.flatten(), color='green', label='NN output')
    ax1.legend()
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Neural Network Output')
    
    # Plot loss curves
    ax2.plot(train_loss_history[:epochs], label='Training Loss')
    ax2.plot(val_loss_history[:epochs], label='Validation Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.set_title('Loss Curves')
    ax2.set_yscale('log')
    ax2.legend()
    
    plt.tight_layout()
    return fig

def train_model(hidden_dims, learning_rate, epochs):
    model = SimpleNN(hidden_dims)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    x_train_tensor = torch.tensor(x_train.reshape(-1, 1), dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32)
    x_val_tensor = torch.tensor(x_val.reshape(-1, 1), dtype=torch.float32)
    y_val_tensor = torch.tensor(y_val.reshape(-1, 1), dtype=torch.float32)
    
    train_loss_history = []
    val_loss_history = []
    model_weights_history = []
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(x_train_tensor)
        loss = criterion(outputs, y_train_tensor)
        loss.backward()
        optimizer.step()
        train_loss_history.append(loss.item())
        
        model.eval()
        with torch.no_grad():
            val_outputs = model(x_val_tensor)
            val_loss = criterion(val_outputs, y_val_tensor)
            val_loss_history.append(val_loss.item())
        
        # Save model weights
        model_weights_history.append([param.clone().detach().numpy() for param in model.parameters()])
    
    return model, train_loss_history, val_loss_history, model_weights_history

def parse_hidden_dims(hidden_dims_str):
    try:
        return [int(dim) for dim in hidden_dims_str.split(',')]
    except ValueError:
        return [2]  # Default value if parsing fails

def update_visualization(learning_rate, hidden_dims, test_split, data_type):
    global x, y, x_train, x_val, y_train, y_val
    
    # Generate new data
    x, y = generate_data(data_type)
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=test_split, random_state=0)
    
    # Parse hidden dimensions
    hidden_dims = parse_hidden_dims(hidden_dims)
    
    # Train model
    model, train_loss_history, val_loss_history, model_weights_history = train_model(hidden_dims, learning_rate, 1000)
    
    # Create visualization
    fig = visualize_network(model, x_train, y_train, x_val, y_val, train_loss_history, val_loss_history, 1000)
    return fig

def create_animation(learning_rate, hidden_dims, test_split, data_type, epochs_per_frame, frame_interval):
    global x, y, x_train, x_val, y_train, y_val
    
    # Generate new data
    x, y = generate_data(data_type)
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=test_split, random_state=0)
    
    # Parse hidden dimensions
    hidden_dims = parse_hidden_dims(hidden_dims)
    
    # Train model
    model, train_loss_history, val_loss_history, model_weights_history = train_model(hidden_dims, learning_rate, 1000)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    
    # Plot network output
    ax1.scatter(x_train, y_train, color='blue', label='Train set')
    ax1.scatter(x_val, y_val, color='red', label='Validation set')
    
    x_range = np.linspace(-10, 10, 1000).reshape(-1, 1)
    x_range_tensor = torch.tensor(x_range, dtype=torch.float32)
    
    def animate(frame):
        epoch = frame * epochs_per_frame
        ax1.clear()
        ax2.clear()
        
        # Update model weights
        for param, weight in zip(model.parameters(), model_weights_history[epoch]):
            param.data = torch.tensor(weight)
        
        y_pred = model(x_range_tensor).detach().numpy()
        ax1.plot(x_range, y_pred.flatten(), color='green', label='NN output')
        ax1.scatter(x_train, y_train, color='blue', label='Train set')
        ax1.scatter(x_val, y_val, color='red', label='Validation set')
        ax1.legend()
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('Neural Network Output')
        
        ax2.plot(train_loss_history[:epoch], label='Training Loss')
        ax2.plot(val_loss_history[:epoch], label='Validation Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.set_title('Loss Curves')
        ax2.set_yscale('log')
        ax2.legend()
        
        plt.tight_layout()
        return fig
    
    ani = animation.FuncAnimation(fig, animate, frames=1000 // epochs_per_frame, interval=frame_interval, repeat=False)
    
    # Save animation as gif
    ani.save('training_animation.gif', writer='imagemagick')
    
    # Return path to saved gif
    return 'training_animation.gif'

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("""
    # Neural Network Training Visualizer
    
    This interactive tool allows you to visualize the training process of a neural network on different types of data.
    You can adjust various parameters like learning rate, network architecture, and visualization settings to see how
    they affect the learning process. The animation shows both the network's predictions and the loss curves in real-time.
    
    ## Parameters:
    - Learning Rate: Controls how much the model adjusts its weights in each training step
    - Hidden Dimensions: Defines the architecture of the neural network (e.g., "3,3" creates two hidden layers with 3 neurons each)
    - Test Split: Portion of data used for validation
    - Data Type: Type of function to learn (quadratic, linear, sinusoidal, exponential, or random)
    - Epochs per Frame: Number of training epochs between animation frames
    - Frame Interval: Time between animation frames in milliseconds
    """)
    
    with gr.Row():
        lr_number = gr.Number(value=0.01, label="Learning Rate")
        hidden_dims_text = gr.Textbox(value="2", label="Hidden Dimensions (e.g: 3, 3)")
        test_split_slider = gr.Slider(minimum=0.05, maximum=0.5, step=0.05, value=0.1, label="Test Split")
        data_type_dropdown = gr.Dropdown(choices=['quadratic', 'linear', 'sinusoidal', 'exponential', 'random'], 
                                       value='quadratic', label="Data Type")
        epochs_per_frame_slider = gr.Slider(minimum=1, maximum=100, step=1, value=100, label="Epochs per Frame")
        frame_interval_slider = gr.Slider(minimum=100, maximum=2000, step=100, value=500, label="Frame Interval (ms)")
    
    animation_output = gr.Image()
    
    # Update whenever any input changes
    for input_component in [lr_number, hidden_dims_text, test_split_slider, data_type_dropdown, epochs_per_frame_slider, frame_interval_slider]:
        input_component.change(
            fn=create_animation,
            inputs=[lr_number, hidden_dims_text, test_split_slider, data_type_dropdown, epochs_per_frame_slider, frame_interval_slider],
            outputs=animation_output
        )

if __name__ == "__main__":
    iface.launch()

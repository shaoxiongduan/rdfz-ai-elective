# Class 4 Gomoku AI with CNN

In this class, we will learn how to build a Gomoku AI with CNN and Cursor, the AI code editor.

## 1. Gomoku

Gomoku is a board game, also known as Five in a Row. It is a two-player game, played on a 15x15 board. The game is played by two players, who take turns placing stones of their color on the board. The goal of the game is to be the first to form a line of five stones in a row, column, or diagonal.

## 2. Gomoku AI

We will use a CNN to predict the next move of the game. The CNN will take the current board state as input, and output the probability of each position to be a valid move.


# Some Features to Implement

## Elements
1. Main Menu: Players can choose between two game modes:
- Play with Person (PvP)
- Play with AI

2. Game Board: A 20x20 grid where players take turns placing their stones.
3. Turn Indicator: Displays whose turn it is (Black or White).
4. Win Detection: Automatically detects when a player has five stones in a row (horizontally, vertically, or diagonally).
5. Game Over Screen: Shows the winner and offers a button to return to the main menu.

## AI Implementation
The AI uses a CNN to predict the best move based on the current board state.
The model is trained on a dataset of Gomoku games.
Players can choose to play against this AI opponent.

## How It Works
The program starts by loading a pre-trained model or training a new one if specified.
In the main game loop:
1. Players can place stones on the board by clicking.
2. The AI calculates its move when it's the computer's turn.
The game checks for a win condition after each move.
3. The game continues until a player wins or the players return to the main menu.

# Game Demo

<video controls src="demo.mp4" title="Title"></video>

# Prompting References

[My prompts](prompts.md)
# Environment Setup

# 🚀 AI Elective: Environment Setup and PyTorch Tutorial

Welcome to the exciting world of AI! 🤖 This tutorial will guide you through setting up your Python environment, installing PyTorch, and downloading Cursor. We've got you covered whether you're on Windows 🖥️ or macOS 🍎.

## Table of Contents

1. [Installing Python 🐍](#installing-python-)
2. [Creating a Virtual Environment 🏠](#creating-a-virtual-environment-)
3. [Installing PyTorch 🔥](#installing-pytorch-)
4. [Downloading Cursor](#downloading-cursor)

## Installing Python 🐍

### Windows 🖥️

1. Visit the official Python website: [Python for Windows](https://www.python.org/downloads/windows/)
2. Download the latest Python 3 installer (64-bit version recommended)
3. Run the installer
4. ✅ Check the box that says "Add Python to PATH"
5. Click "Install Now"

### MacOS 🍎

1. Go to Python [downloads](https://www.python.org/downloads/) site.
2. Download the MacOS installer (.pkg)
3. Run the installation wizard and follow the instructions.

**Or**

1. Install Homebrew if you haven't already:
	1. Go to https://brew.sh/ and follow the installation instructions
2. Use Homebrew to install Python:
    
    ```bash
    brew install python
    ```
    

📚 Learn more about Python: [Python Documentation](https://docs.python.org/3/)

## Creating a Virtual Environment 🏠

Virtual environments help you manage dependencies for different projects. Here's how to create and activate one:

### Windows 🖥️

1. Open Command Prompt
2. Navigate to your project directory
3. Create a virtual environment:
    
    ```bash
    python -m venv myenv
    ```
    
4. Activate the virtual environment:
    
    ```bash
    myenv\\Scripts\\activate
    ```
    

### macOS 🍎

1. Open Terminal
2. Navigate to your project directory
3. Create a virtual environment:
    
    ```bash
    python3 -m venv myenv
    ```
    
4. Activate the virtual environment:
    
    ```bash
    source myenv/bin/activate
    ```
    

🔗 Learn more about virtual environments: [Python venv](https://docs.python.org/3/library/venv.html)

## Installing PyTorch 🔥

With your virtual environment activated:

1. Visit the PyTorch website: [PyTorch Get Started](https://pytorch.org/get-started/locally/)
2. Select your preferences (Stable build, your OS, pip, Python, CUDA None)
3. Copy the provided command and run it in your terminal or command prompt

For example:

```bash
pip3 install torch torchvision torchaudio
```

📘 PyTorch Documentation: [PyTorch Docs](https://pytorch.org/docs/stable/index.html)

### Running a Simple Neural Network Example 🧠

Now that you have PyTorch installed, let's create a simple neural network. Create a new file called `simple_nn.py` and add the following code:

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Create random input data and target
input_data = torch.randn(100, 10)
target = torch.randn(100, 1)

# Initialize the model, loss function, and optimizer
model = SimpleNN()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training loop
for epoch in range(100):
    # Forward pass
    output = model(input_data)
    loss = criterion(output, target)

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')

print("Training complete!")

```

To run this example:

1. Make sure your virtual environment is activated
2. Save the code above in a file named `simple_nn.py`
3. Run the script:
    
    ```bash
    python simple_nn.py
    ```
    

You should see the loss decreasing as the network trains. 📉

🎓 Learn more about neural networks: [Neural Networks Explained](https://www.ibm.com/cloud/learn/neural-networks)

Congratulations! You've now set up your Python environment, installed PyTorch, and run a simple neural network example. You're on your way to becoming an AI expert! 🦾

### Additional Resources 📚

- [Deep Learning with PyTorch](https://pytorch.org/deep-learning-with-pytorch)
- [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)
- [Kaggle Learn](https://www.kaggle.com/learn)

Happy coding and exploring the fascinating world of AI! 🌟

## Downloading Cursor

Cursor is The AI Code Editor, achieving seamless integration between VSCode and state-of-the-art LLMs including [ChatGPT-4o](https://openai.com/index/hello-gpt-4o/) and [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet).

1. Visit the Cursor official website: [Cursor](https://www.cursor.com/)
2. Download Cursor installer for your OS and run the installer.
3. [Optional] If you previously use VSCode, you can migrate your settings, themes and extensions on the app.
4. If you have paid accounts to OpenAI, Anthropic, Google, or Azure, you can generate an API key with your account to use paid models in Cursor.
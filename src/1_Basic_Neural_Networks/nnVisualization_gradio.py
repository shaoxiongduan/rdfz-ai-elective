import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid main thread issues
import matplotlib.pyplot as plt
import gradio as gr

# Title for the Gradio app
title = "Neural Network Visualizer"

# Generate random data centered around origin
np.random.seed(0)
num_points = 200
X = 2 * np.random.rand(num_points, 2) - 1  # Scale to [-1,1]
y = (X[:, 1] > -0.5 * X[:, 0]).astype(int)  # Simplified boundary through origin

# Generate nonlinear data
X_nonlinear = 2 * np.random.rand(num_points, 2) - 1  # Scale to [-1,1]
y_nonlinear = (X_nonlinear[:, 1] > 0.5 * np.sin(4 * X_nonlinear[:, 0])).astype(int)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def no_activation(x):
    return x

activation_functions = {
    "None": no_activation,
    "ReLU": relu,
    "Sigmoid": sigmoid
}

class SimpleNN:
    def __init__(self):
        self.weights = np.array([-1.0, 1.0])  # Initialize with diagonal line
        self.bias = 0.0  # Changed to center decision boundary
        
    def forward(self, X, activation="Sigmoid"):
        z = np.dot(X, self.weights) + self.bias
        return activation_functions[activation](z)
    
    def predict(self, X, activation="Sigmoid"):
        return (self.forward(X, activation) > 0.5).astype(int)

class HiddenLayerNN:
    def __init__(self):
        # Initialize with weights that create a curved decision boundary
        self.weights1 = np.array([[1.0, -1.0], [-1.0, 1.0]])
        self.bias1 = np.array([0.0, 0.0])
        self.weights2 = np.array([[1.0], [1.0]])
        self.bias2 = np.array([0.0])  # Changed to center decision boundary
    
    def forward(self, X, activation="Sigmoid"):
        hidden = X @ self.weights1 + self.bias1
        hidden = activation_functions[activation](hidden)
        output = hidden @ self.weights2 + self.bias2
        return sigmoid(output)
    
    def predict(self, X, activation="Sigmoid"):
        return (self.forward(X, activation) > 0.5).astype(int)

simple_nn = SimpleNN()
hidden_nn = HiddenLayerNN()

def visualize_simple_nn(w1, w2, b, activation):
    simple_nn.weights = np.array([w1, w2])
    simple_nn.bias = b
    
    # Create meshgrid centered at origin
    xx, yy = np.meshgrid(np.linspace(-1.2, 1.2, 140), np.linspace(-1.2, 1.2, 140))
    X_mesh = np.c_[xx.ravel(), yy.ravel()]
    
    # Make predictions
    Z = simple_nn.predict(X_mesh, activation).reshape(xx.shape)
    predictions = simple_nn.predict(X, activation)
    accuracy = np.mean(predictions == y) * 100
    
    # Create figure
    fig = plt.figure(figsize=(12, 5))
    
    # Plot decision boundary
    plt.subplot(121)
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.RdYlBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolor='black')
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.title(f'Decision Boundary (Accuracy: {accuracy:.2f}%)')
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Visualize neural network
    plt.subplot(122)
    plt.axis('off')
    plt.text(0.1, 0.9, 'Input Layer', ha='center', va='center', fontsize=12, fontweight='bold')
    plt.text(0.9, 0.9, f'Output Layer\n({activation})', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw neurons and connections
    plt.plot([0.2, 0.2], [0.7, 0.8], 'ko-')
    plt.text(0.1, 0.75, 'X1', ha='right', va='center')
    plt.plot([0.2, 0.2], [0.5, 0.6], 'ko-')
    plt.text(0.1, 0.55, 'X2', ha='right', va='center')
    plt.plot([0.8, 0.8], [0.6, 0.7], 'ko-')
    plt.text(0.9, 0.65, 'Y', ha='left', va='center')
    plt.plot([0.2, 0.8], [0.75, 0.65], 'b-', alpha=abs(w1)/2)
    plt.plot([0.2, 0.8], [0.55, 0.65], 'b-', alpha=abs(w2)/2)
    
    plt.tight_layout()
    return fig

def visualize_hidden_nn(w11, w12, w13, w14, w21, w22, b11, b12, b21, activation):
    hidden_nn.weights1 = np.array([[w11, w12], [w13, w14]])
    hidden_nn.bias1 = np.array([b11, b12])
    hidden_nn.weights2 = np.array([[w21], [w22]])
    hidden_nn.bias2 = np.array([b21])
    
    # Create meshgrid centered at origin
    xx, yy = np.meshgrid(np.linspace(-1.2, 1.2, 140), np.linspace(-1.2, 1.2, 140))
    X_mesh = np.c_[xx.ravel(), yy.ravel()]
    
    # Make predictions
    Z = hidden_nn.predict(X_mesh, activation).reshape(xx.shape)
    predictions = hidden_nn.predict(X_nonlinear, activation)
    accuracy = np.mean(predictions == y_nonlinear) * 100
    
    # Create figure
    fig = plt.figure(figsize=(12, 5))
    
    # Plot decision boundary
    plt.subplot(121)
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.RdYlBu)
    plt.scatter(X_nonlinear[:, 0], X_nonlinear[:, 1], c=y_nonlinear, cmap=plt.cm.RdYlBu, edgecolor='black')
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.title(f'Decision Boundary (Accuracy: {accuracy:.2f}%)')
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Visualize neural network
    plt.subplot(122)
    plt.axis('off')
    plt.text(0.1, 0.9, 'Input Layer', ha='center', va='center', fontsize=12, fontweight='bold')
    plt.text(0.5, 0.9, f'Hidden Layer\n({activation})', ha='center', va='center', fontsize=12, fontweight='bold')
    plt.text(0.9, 0.9, 'Output Layer\n(Sigmoid)', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw neurons
    for i, y_pos in enumerate([0.75, 0.55]):
        plt.plot([0.2, 0.2], [y_pos-0.05, y_pos+0.05], 'ko-')
        plt.text(0.1, y_pos, f'X{i+1}', ha='right', va='center')
    
    for i, y_pos in enumerate([0.75, 0.55]):
        plt.plot([0.5, 0.5], [y_pos-0.05, y_pos+0.05], 'ko-')
        plt.text(0.4, y_pos, f'H{i+1}', ha='right', va='center')
    
    plt.plot([0.8, 0.8], [0.65-0.05, 0.65+0.05], 'ko-')
    plt.text(0.9, 0.65, 'Y', ha='left', va='center')
    
    # Draw connections with varying thickness
    weights1 = hidden_nn.weights1.flatten()
    weights2 = hidden_nn.weights2.flatten()
    
    # Input to hidden connections
    for i, y1 in enumerate([0.75, 0.55]):
        for j, y2 in enumerate([0.75, 0.55]):
            plt.plot([0.2, 0.5], [y1, y2], 'b-', alpha=abs(weights1[i*2 + j])/2)
    
    # Hidden to output connections
    for i, y1 in enumerate([0.75, 0.55]):
        plt.plot([0.5, 0.8], [y1, 0.65], 'b-', alpha=abs(weights2[i])/2)
    
    plt.tight_layout()
    return fig

# Create Gradio interface
with gr.Blocks(title=title) as iface:
    gr.Markdown(f"# {title}")
    
    with gr.Row():
        network_type = gr.Radio(["Simple Network", "Network with Hidden Layer"], value="Simple Network", label="Network Type")
        activation = gr.Dropdown(choices=list(activation_functions.keys()), value="Sigmoid", label="Activation Function")
    
    with gr.Row() as simple_controls:
        w1_slider = gr.Slider(-2, 2, step=0.1, value=-1.0, label="Weight 1")
        w2_slider = gr.Slider(-2, 2, step=0.1, value=1.0, label="Weight 2")
        b_slider = gr.Slider(-2, 2, step=0.1, value=0.0, label="Bias")
    
    with gr.Row(visible=False) as hidden_controls:
        with gr.Column():
            # First layer weights
            w11_slider = gr.Slider(-2, 2, step=0.01, value=1.0, label="Input 1 to Hidden 1")
            w12_slider = gr.Slider(-2, 2, step=0.01, value=-1.0, label="Input 1 to Hidden 2")
            w13_slider = gr.Slider(-2, 2, step=0.01, value=-1.0, label="Input 2 to Hidden 1")
            w14_slider = gr.Slider(-2, 2, step=0.01, value=1.0, label="Input 2 to Hidden 2")
            
            # First layer biases
            b11_slider = gr.Slider(-2, 2, step=0.01, value=0.0, label="Hidden 1 Bias")
            b12_slider = gr.Slider(-2, 2, step=0.01, value=0.0, label="Hidden 2 Bias")
            
        with gr.Column():
            # Second layer weights
            w21_slider = gr.Slider(-2, 2, step=0.01, value=1.0, label="Hidden 1 to Output")
            w22_slider = gr.Slider(-2, 2, step=0.01, value=1.0, label="Hidden 2 to Output")
            
            # Output bias
            b21_slider = gr.Slider(-2, 2, step=0.01, value=0.0, label="Output Bias")
    
    plot_output = gr.Plot()
    
    def update_network_type(choice):
        if choice == "Simple Network":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
    
    network_type.change(
        fn=update_network_type,
        inputs=network_type,
        outputs=[simple_controls, hidden_controls]
    )
    
    def update_plot(network_type, w1, w2, b, w11, w12, w13, w14, w21, w22, b11, b12, b21, activation_type):
        plt.close('all')  # Close all figures before creating new ones
        if network_type == "Simple Network":
            return visualize_simple_nn(w1, w2, b, activation_type)
        else:
            return visualize_hidden_nn(w11, w12, w13, w14, w21, w22, b11, b12, b21, activation_type)
    
    # Update plot when any input changes
    all_inputs = [network_type, w1_slider, w2_slider, b_slider, 
                 w11_slider, w12_slider, w13_slider, w14_slider,
                 w21_slider, w22_slider,
                 b11_slider, b12_slider, b21_slider,
                 activation]
    
    for input_component in all_inputs:
        input_component.change(
            fn=update_plot,
            inputs=all_inputs,
            outputs=plot_output
        )
    
    gr.Markdown("""
    Explore how neural networks make decisions by adjusting their parameters:
    
    - Choose between a simple network and one with a hidden layer
    - Select different activation functions
    - Use the sliders to modify weights and biases
    - The left plot shows the decision boundary and data points
    - The right plot visualizes the network architecture
    - Line thickness represents weight magnitude
    """)

if __name__ == "__main__":
    iface.launch()

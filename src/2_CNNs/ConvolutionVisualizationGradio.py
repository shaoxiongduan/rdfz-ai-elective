import gradio as gr
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

def apply_convolution(image, *kernel_values):
    # Convert kernel values from list to numpy array and reshape to 3x3
    kernel = np.array(kernel_values).reshape(3, 3)
    
    gray_image = image.convert("L")
    
    # Convert image and kernel to torch tensors
    img_tensor = torch.tensor(np.array(gray_image), dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    kernel_tensor = torch.tensor(kernel, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    
    # Apply convolution using torch conv2d
    convolved = F.conv2d(img_tensor, kernel_tensor, padding=1)
    
    # Convert back to numpy array
    convolved = convolved.squeeze().numpy()
    
    convolved_pil = Image.fromarray(convolved)
    
    return gray_image, convolved_pil

# Default kernel values
default_kernel = [1, -1, 1, -1, 1, -1, 1, -1, 1]

# Create the interface
with gr.Blocks() as demo:
    gr.Markdown("# Image Convolution Visualization")
    
    with gr.Row():
        image_input = gr.Image(label="Input Image", type="pil")
        
    # Display kernel inputs in a 3x3 grid using 3 gr.Rows
    num_inputs = []
    for i in range(3):
        with gr.Row():
            for j in range(3):
                num_inputs.append(gr.Number(label=f"Kernel Value ({i+1},{j+1})", value=default_kernel[i*3 + j]))
    
    with gr.Row():
        grayscale_output = gr.Image(label="Grayscale Image", type="pil")
        convolved_output = gr.Image(label="Convolved Image", type="pil")
    
    # Button to trigger processing
    process_btn = gr.Button("Apply Convolution")
    
    # Set up the click event
    process_btn.click(
        fn=apply_convolution,
        inputs=[image_input, *num_inputs],
        outputs=[grayscale_output, convolved_output]
    )

demo.launch()

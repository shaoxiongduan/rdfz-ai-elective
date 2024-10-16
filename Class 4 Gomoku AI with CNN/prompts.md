# Prompts

# Creating the Game

I first start with prompting the game:
![alt text](<prompts/Screenshot 2024-10-15 at 09.43.25.png>) 

This is the result I get:
<video controls src="prompts/Screen Recording 2024-10-15 at 09.43.38.mp4" title="Title"></video>

The pieces are not on the intersections of the lines (IDK if this is the right way of playing gomoku, I just like my pieces on the grid intersections). So I ask it to make the pieces on the intersections:
![alt text](<prompts/Screenshot 2024-10-15 at 09.45.46.png>) 

Much better now!
<video controls src="prompts/Screen Recording 2024-10-15 at 09.47.06.mp4" title="Title"></video>

Then I move on to making the main menu and turn display:
![alt text](<prompts/Screenshot 2024-10-15 at 09.48.13.png>)

I get this result:
<video controls src="prompts/Screen Recording 2024-10-15 at 09.48.57.mp4" title="Title"></video>

But it is not fully working! When I click on "Main Menu", it takes me straight back to another game. So I ask it to fix it:
![alt text](<prompts/Screenshot 2024-10-15 at 09.50.23.png>) 

![alt text](<prompts/Screenshot 2024-10-15 at 09.50.56.png>) 
![alt text](<prompts/Screenshot 2024-10-15 at 10.05.43.png>) 
After some debugging, I figured out that the buttons for the main menu and play with ai are overlapped. So it instantly registers the two buttons when I make a click. A simple offset fixed this.
<video controls src="prompts/Screen Recording 2024-10-15 at 10.05.47.mp4" title="Title"></video>

# Creating the AI
Now we have a working game, we start making the AI.
For this I chose to use a CNN, and that's what I prompted:
![alt text](<prompts/Screenshot 2024-10-15 at 14.33.02.png>) 

But it is giving me this error:
![alt text](<prompts/Screenshot 2024-10-15 at 14.33.18.png>) 

We can take a look at our data for training:
![alt text](<prompts/Screenshot 2024-10-16 at 20.04.34.png>)

Since we are using data from the Freestyle data, the board should be 20x20 instead of 15x15. A simple change of the board size fixed the error.

But when I run the code, it is not outputting anything. This is because though the model is training, we did not ask it to output anything. So I asked it to output the losses and progress using tqdm.

![alt text](<prompts/Screenshot 2024-10-15 at 14.36.04.png>)

![alt text](<prompts/Screenshot 2024-10-15 at 14.36.45.png>) 

After this we get this nice progress bar with the loss printed above it:

![alt text](<prompts/Screenshot 2024-10-15 at 14.52.51.png>) 

But the loss is not going down for some reason. We ask Mr. GPT to fix this.
![alt text](<prompts/Screenshot 2024-10-15 at 14.54.14.png>) 

(TYPO: should be 128 here, but it realized I made a mistake and corrected it itself)
![alt text](<prompts/Screenshot 2024-10-15 at 14.54.18.png>) 

It now sorta works.
![alt text](<prompts/Screenshot 2024-10-15 at 14.56.05.png>) 

I then asked it to use cuda or mps if available to speed up the training.
![alt text](<prompts/Screenshot 2024-10-15 at 14.56.54.png>) 

Then I asked it to save the model each 1000 steps so that I can check if the model is doing a good job or not.
![alt text](<prompts/Screenshot 2024-10-15 at 15.03.20.png>) 

I tried to fix the training issue meanwhile:
![alt text](<prompts/Screenshot 2024-10-16 at 08.43.54.png>) 

It didn't work. 
![alt text](<prompts/Screenshot 2024-10-16 at 08.51.03.png>) 

So I switched up my prompt a bit:
![alt text](<prompts/Screenshot 2024-10-16 at 13.45.41.png>) 
Made it fix the error it outputted:
![alt text](<prompts/Screenshot 2024-10-16 at 13.46.33.png>)
And now it works!
![alt text](<prompts/Screenshot 2024-10-16 at 13.48.22.png>) 

I used this prompt to make it work in the end: In cursor you can use @ and choose the files you want the model to reference or you can just drag the file into the prompt.
![alt text](<prompts/Screenshot 2024-10-16 at 14.49.17.png>) 

With that out of the way, I prompted it to implement the logic for the AI to play:
![alt text](<prompts/Screenshot 2024-10-16 at 15.01.04.png>) 

I got this error:
![alt text](<prompts/Screenshot 2024-10-16 at 15.02.07.png>) 
I used a prompt something along the lines of "Fix error: and copied the entire error message in" to get it to work.

But the AI is not making its move everytime.
<video controls src="prompts/Screen Recording 2024-10-16 at 15.05.18.mp4" title="Title"></video>

I asked it to fix this:
![alt text](<prompts/Screenshot 2024-10-16 at 15.06.29.png>) 

And GPT fixed it.

During the process of making the AI play I also encountered this error:

![alt text](<prompts/Screenshot 2024-10-16 at 15.09.04.png>) 
It was because the input tensor and the model are on different devices. A simple .to(device) on the input tensor fixed it.
![alt text](<prompts/Screenshot 2024-10-16 at 15.09.09.png>) 


And now with some game logic fixes, the whole thing is done!
![alt text](<prompts/Screenshot 2024-10-16 at 15.22.31.png>) 


# Final demo

<video controls src="demo.mp4" title="Title"></video>
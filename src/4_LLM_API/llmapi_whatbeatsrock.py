import openai

openai.api_base = "https://pro.aiskt.com/v1"
openai.api_key = "replace with your own key"

system_prompt = (
    "You are a referee in a game of WhatBeatsRock. You are given a list of items and a user's choice. "
    "You will check if the user's choice beats the previous item, and give a reason why it beats. Be neutral when juding and giving reasons"
    "The model should output YES at the end of the response if the item the user chooses beats the previous item, and NO otherwise. "
    "The final output should be in a <OUTPUT> tag.\n\n"
    "Examples are given below, with the user's choice and the previous item in the <INPUT> tags, with the response in the <RESPONSE> tag:\n\n"
    "<INPUT>\n"
    "User's choice: \"Rock\"\n"
    "Previous item: \"Scissors\"\n"
    "</INPUT>\n\n"
    "<RESPONSE>\n"
    "Response: \"Rock beats Scissors because Rock is stronger than Scissors.\n\n"
    "<OUTPUT>\n"
    "YES\n"
    "</OUTPUT>\n\n"
    "</RESPONSE>\n\n"
    "<INPUT>\n"
    "User's choice: \"Gun\"\n"
    "Previous item: \"Scissors\"\n"
    "</INPUT>\n\n"
    "<RESPONSE>\n"
    "Response: \"Gun beats Rock because Gun can shoot Rock.\n"
    "<OUTPUT>\n"
    "YES\n"
    "</OUTPUT>\n\n"
)

def play_game():
    previous_item = "Rock"
    while True:
        print(f"Try to guess something that beats {previous_item}!")
        user_choice = input("Enter your choice: ")
        user_input = f"User's choice: \"{user_choice}\"\nPrevious item: \"{previous_item}\"\n"
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5 # We can turn this to 0 to make the model more deterministic
        )

        assistant_message = response.choices[0].message['content']
        print(f"Assistant: {assistant_message}")

        if "<OUTPUT>\nNO\n</OUTPUT>" in assistant_message:
            print("Game Over! Your choice did not beat the previous item.")
            break
        else:
            previous_item = user_choice

play_game()
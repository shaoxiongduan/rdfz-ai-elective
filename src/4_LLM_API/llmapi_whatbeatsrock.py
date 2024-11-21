import openai
import streamlit as st

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

st.title("What Beats Rock Game")
st.write("Try to enter items that beat the previous item!")

if 'previous_item' not in st.session_state:
    st.session_state.previous_item = "Rock"
    st.session_state.game_over = False
    st.session_state.reason = None

# Display current item in a prominent info box
st.info(f"🎯 Current item to beat: **{st.session_state.previous_item}**")

# Display the previous reason if it exists
if st.session_state.reason:
    st.success(f"💡 Previous winning reason: {st.session_state.reason}")

if not st.session_state.game_over:
    user_choice = st.text_input("Enter your choice:", key="user_input")
    
    if st.button("Submit"):
        user_input = f"User's choice: \"{user_choice}\"\nPrevious item: \"{st.session_state.previous_item}\"\n"
        
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
        
        # Extract the reason from the response
        reason_start = assistant_message.find("Response: \"") + 10
        reason_end = assistant_message.find("\n", reason_start)
        reason = assistant_message[reason_start:reason_end].strip('"')

        if "<OUTPUT>\nNO\n</OUTPUT>" in assistant_message:
            st.error("❌ Game Over! Your choice did not beat the previous item.")
            st.session_state.game_over = True
            st.session_state.reason = None
        else:
            st.session_state.previous_item = user_choice
            st.session_state.reason = reason
            st.success("✅ Good job! Enter another item!")
            # Force a rerun to update the current item display immediately
            st.rerun()

if st.session_state.game_over:
    if st.button("Play Again"):
        st.session_state.previous_item = "Rock"
        st.session_state.game_over = False
        st.session_state.reason = None
        st.rerun()
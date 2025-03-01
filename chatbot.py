import streamlit as st
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🚨 API Key is missing! Please check your .env file.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)

# Define the model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")  # Change to "gemini-1.5-flash" if needed
except Exception as e:
    st.error(f"⚠️ Model loading error: {e}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", layout="centered")

st.title("🤖 AI Chatbot")
st.write("Chat with AI and fix your problems!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stop_response" not in st.session_state:
    st.session_state.stop_response = False

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input with stop button
col1, col2 = st.columns([8, 2])  # Adjust width ratio for buttons

with col1:
    user_input = st.chat_input("Type your message here...")

with col2:
    stop_btn = st.button("🛑 Stop", key="stop_button", use_container_width=True)

# Stop response logic
if stop_btn:
    st.session_state.stop_response = True

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)

    # Generate response from Gemini
    try:
        st.session_state.stop_response = False  # Reset stop flag
        with st.chat_message("assistant"):
            response_area = st.empty()  # Placeholder for response
            
            # Thinking animation
            for dots in ["Responding.", "Responding..", "Responding...","Responding.", "Responding..", "Responding..."]:
                response_area.markdown(dots)
                time.sleep(0.7)  # Pause for effect

            response = model.generate_content(user_input)
            
            # Stop response if button is pressed
            if not st.session_state.stop_response:
                bot_reply = response.text
            else:
                bot_reply = "⚠️ Response stopped."

            response_area.markdown(bot_reply)

    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"
        response_area.markdown(bot_reply)

    # Save chat history if not stopped
    if not st.session_state.stop_response:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

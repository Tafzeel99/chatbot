import streamlit as st
import time
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Custom CSS for better UI
def apply_custom_css():
    st.markdown("""
    <style>
        .main-header {
            background-color: #f0f5ff;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 5px solid #4b6fff;
        }
        .chat-container {
            border-radius: 10px;
            background-color: #f9f9f9;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stButton button {
            background-color: #4b6fff;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        .stButton button:hover {
            background-color: #374db7;
            color: white;
        }
        .stop-button button {
            background-color: #ff4b4b;
        }
        .stop-button button:hover {
            background-color: #b73737;
        }
        .clear-button button {
            background-color: #ff9d4b;
        }
        .clear-button button:hover {
            background-color: #b77337;
        }
        .stTextInput input {
            border-radius: 5px;
        }
        .stChatInputContainer {
            margin-top: 1rem;
        }
        .user-avatar {
            background-color: #4b6fff;
            color: white;
            padding: 8px;
            border-radius: 50%;
            display: inline-block;
            text-align: center;
            width: 32px;
            height: 32px;
        }
        .assistant-avatar {
            background-color: #7e57c2;
            color: white;
            padding: 8px;
            border-radius: 50%;
            display: inline-block;
            text-align: center;
            width: 32px;
            height: 32px;
        }
    </style>
    """, unsafe_allow_html=True)

# Configure Gemini AI if API key exists
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
st.set_page_config(
    page_title="AI ChatBot", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Sidebar with options
with st.sidebar:
    # Model settings
    st.subheader("🛠️ Model Settings")
    model_option = st.selectbox(
        "Choose Model", 
        ["gemini-1.5-pro", "gemini-1.5-flash"], 
        index=0
    )
    
    # About section
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown("""
    This AI ChatBot is powered by Google's Gemini models and can help you with:
    - Answering questions
    - Generating creative content
    - Problem solving
    - And much more!
    
    Ask anything and get helpful responses!
    """)
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 AI Chatbot by @tafzeel")

# Main content
st.markdown("<div class='main-header'><h1 style='color: black;'>🤖 Smart AI ChatBot</h1><p style='color: black;'>Your intelligent companion for any question or task. What can I help you today?</p></div>", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stop_response" not in st.session_state:
    st.session_state.stop_response = False


# Display chat history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    avatar_class = "user-avatar" if msg["role"] == "user" else "assistant-avatar"
    
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

st.markdown("</div>", unsafe_allow_html=True)

# User input with control buttons
col1, col2, col3 = st.columns([7, 1.5, 1.5])  # Adjust ratio for buttons

with col1:
    user_input = st.chat_input("Ask me anything...")

with col2:
    stop_btn_placeholder = st.empty()
    stop_btn = stop_btn_placeholder.button(
        "🛑 Stop", 
        key="stop_button", 
        use_container_width=True,
        help="Stop the AI from generating more content"
    )

with col3:
    clear_btn = st.button(
        "🧹 Clear Chat", 
        key="clear_button", 
        use_container_width=True,
        help="Clear the entire conversation history"
    )
    
    # Add CSS class to buttons
    st.markdown("""
    <style>
    [data-testid="stButton"] button:nth-child(1) {
        background-color: #ff4b4b;
    }
    [data-testid="stButton"] button:nth-child(2) {
        background-color: #ff9d4b;
    }
    </style>
    """, unsafe_allow_html=True)

# Clear chat history
if clear_btn:
    st.session_state.messages = []
    st.rerun()  # Rerun to update the UI

# Stop response logic
if stop_btn:
    st.session_state.stop_response = True

# Handle user input
if user_input:
    # Display user message
    st.chat_message("user", avatar="👤").markdown(user_input)

    # Generate response from Gemini
    try:
        st.session_state.stop_response = False  # Reset stop flag
        with st.chat_message("assistant", avatar="🤖"):
            response_area = st.empty()  # Placeholder for response
            
            # Improved thinking animation
            thinking_messages = [
                "Thinking.",
                "Thinking..",
                "Thinking...",
                "Almost there.",
                "Almost there..",
                "Almost there...",
                "Almost there.",
                "Almost there..",
                "Almost there...",
                "Almost there.",
                "Almost there..",
                "Almost there...",

            ]
            
            for i in range(3):  # Display 3 random thinking messages
                message = random.choice(thinking_messages)
                response_area.markdown(f"*{message}*")
                time.sleep(0.5)  # Shorter pause for better UX

            # Generate content with selected parameters
            response = model.generate_content(
                user_input,
                generation_config=genai.types.GenerationConfig(
                )
            )
            
            # Stop response if button is pressed
            if not st.session_state.stop_response:
                bot_reply = response.text
            else:
                bot_reply = "⚠️ Response stopped by user."

            response_area.markdown(bot_reply)

    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"
        response_area.markdown(bot_reply)

    # Save chat history if not stopped
    if not st.session_state.stop_response:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

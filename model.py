import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("API key not found! Please set GOOGLE_GENAI_API_KEY in your .env file.")
    st.stop()

# Streamlit page setup
st.set_page_config(page_title="🌸 ManoSakhi - Hindi Mental Health Bot 🌸", layout="wide")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

# Initialize GenAI client
client = genai.Client(api_key=api_key)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to chat (always in Hindi)
def chat_with_ai(user_input):
    conversation = [
        {
            "role": "system",
            "parts": [{"text": (
                "आप एक सहानुभूतिपूर्ण मित्र हैं। "
                "उपयोगकर्ता ने अपनी समस्या साझा की है। "
                "उसे समझाने, प्रोत्साहित करने और सुझाव देने वाला उत्तर दें। "
                "उत्तर हमेशा हिंदी में दें।"
            )}]
        },
        {
            "role": "user",
            "parts": [{"text": user_input}]
        }
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=conversation
    )
    bot_text = response.text

    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

# User input
user_input = st.text_input("कैसा महसूस कर रहे हैं? (हिंदी में लिखें)", key="input_box")

if st.button("Send") and user_input.strip():
    chat_with_ai(user_input)
    st.session_state.input_box = ""  # Clear input after sending

# Chat UI
chat_box_style = """
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    width: 60%;
    color: black;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
"""

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align: right; background-color: #ABEBC6; {chat_box_style} float: right;'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #FFE5B4; {chat_box_style} float: left;'>{msg['text']}</div>",
            unsafe_allow_html=True
        )

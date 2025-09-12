import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import streamlit as st
import google.generativeai as genai  

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("API key not found! Please set GOOGLE_GENAI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="🌸 ManoSakhi - Hindi Mental Health Bot 🌸")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_ai(user_input):
    # Short, empathetic reply in Hindi
    user_input_hindi = (
        f"आप हमेशा संक्षिप्त (2-3 वाक्य), सरल और सहानुभूतिपूर्ण हिंदी में उत्तर दें। "
        f"उपयोगकर्ता कहता है: {user_input}"
    )

    response = model.generate_content(user_input_hindi)
    bot_text = response.text.strip()

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # Speak reply
    try:
        tts = gTTS(bot_text, lang="hi")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        st.audio(tmp_file.name)
    except Exception as e:
        st.error(f"Voice output error: {e}")

# User input
user_input = st.text_input("✍️ यहाँ लिखें (हिंदी या अंग्रेज़ी में)")

if st.button("Send") and user_input.strip():
    chat_with_ai(user_input)

# Chat styling
chat_box_style = """
    border-radius: 12px;
    padding: 10px;
    margin: 8px 0;
    width: 70%;
    color: black;
    font-size: 16px;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.15);
"""

# Display chat bubbles
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background-color: #ABEBC6; text-align: right; margin-left: 30%; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color: #FFE5B4; text-align: left; margin-right: 30%; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )

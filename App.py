import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import streamlit as st
import google.generativeai as genai  # ✅ Correct import

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
    # Force reply in empathetic, natural Hindi
    user_input_hindi = f"आप हमेशा सरल, स्वाभाविक और सहानुभूतिपूर्ण हिंदी में उत्तर दें। उपयोगकर्ता कहता है: {user_input}"

    response = model.generate_content(user_input_hindi)
    bot_text = response.text.strip()

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # Speak reply
    tts = gTTS(bot_text, lang="hi")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    st.audio(tmp_file.name)

# User input
user_input = st.text_input("कैसा महसूस कर रहे हैं? (हिंदी या अंग्रेज़ी में लिखें)")

if st.button("Send") and user_input.strip():
    chat_with_ai(user_input)

# Chat styling
chat_box_style = """
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    width: 60%;
    color: black;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
"""

# Display chat bubbles
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align: right; background-color: #ABEBC6; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #FFE5B4; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )

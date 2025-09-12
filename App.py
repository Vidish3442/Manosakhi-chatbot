import streamlit as st
import os
import tempfile
import base64
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("API key not found! Please set GOOGLE_GENAI_API_KEY in your .env file.")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="🌸 ManoSakhi - Hindi Audio Chatbot 🌸")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

# Init Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Save conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Speech-to-Text (uploaded audio file)
def recognize_speech_from_file(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        # First try Hindi
        text = recognizer.recognize_google(audio, language="hi-IN")
        return text
    except sr.UnknownValueError:
        try:
            # Fallback to English
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
        except:
            return "माफ़ कीजिए, मैं समझ नहीं पाया।"
    except sr.RequestError:
        return "स्पीच सर्विस उपलब्ध नहीं है।"

# Gemini Chat + Hindi TTS
def chat_with_ai(user_text):
    response = model.generate_content(
        f"Translate this into Hindi and reply naturally in Hindi: {user_text}"
    )
    bot_text = response.text

    # Save chat
    st.session_state.chat_history.append({"role": "user", "text": user_text})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # TTS for bot reply
    tts = gTTS(bot_text, lang="hi")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)

    # Convert to base64 for autoplay
    with open(tmp_file.name, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()

    st.markdown(
        f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ---- User Input Options ----
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("🎤 अपनी आवाज़ रिकॉर्ड करें और अपलोड करें", type=["wav", "mp3", "m4a"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        user_input = recognize_speech_from_file(tmp_path)
        st.write(f"🗣️ आपने कहा: {user_input}")
        chat_with_ai(user_input)

with col2:
    text_input = st.text_input("✍️ यहाँ लिखें (English या हिंदी में)")
    if st.button("Send ✉️") and text_input.strip():
        chat_with_ai(text_input)

# ---- Chat Bubbles ----
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
            f"<div style='text-align: right; background-color: #ABEBC6; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #FFE5B4; {chat_box_style}'>{msg['text']}</div>",
            unsafe_allow_html=True
        )

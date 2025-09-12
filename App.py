import streamlit as st
import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from google import genai
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

# Init Gemini client
client = genai.Client(api_key=api_key)

# Save conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Speech-to-Text (STT) → English/Hindi input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 कृपया बोलें (English या हिंदी में)...")
        audio = recognizer.listen(source, phrase_time_limit=8)
    try:
        text = recognizer.recognize_google(audio, language="hi-IN")  
        return text
    except sr.UnknownValueError:
        try:
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
        except:
            return "माफ़ कीजिए, मैं समझ नहीं पाया।"
    except sr.RequestError:
        return "स्पीच सर्विस उपलब्ध नहीं है।"

# Gemini Chat + Hindi TTS (auto-play)
def chat_with_ai(user_text):
    conversation = [
        {"role": "user", "parts": [{"text": f"Translate this into Hindi and reply naturally in Hindi: {user_text}"}]}
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=conversation
    )
    bot_text = response.text

    # Save chat
    st.session_state.chat_history.append({"role": "user", "text": user_text})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # TTS for bot reply
    tts = gTTS(bot_text, lang="hi")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)

    # Auto-play with HTML5 <audio autoplay>
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{open(tmp_file.name,'rb').read().hex()}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ---- User Input Options ----
col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ बोलें और भेजें"):
        user_input = recognize_speech()
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
            f"<div style='text-align: right; background-color: #ABEBC6; {chat_box_style} float: right;'>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #FFE5B4; {chat_box_style} float: left;'>{msg['text']}</div>",
            unsafe_allow_html=True
        )

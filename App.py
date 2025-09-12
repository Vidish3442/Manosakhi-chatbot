import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("API key not found! Set GOOGLE_GENAI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="🌸 ManoSakhi - Voice Chatbot 🌸")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

# Session state to store chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function: Speech-to-Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 बोलें (English या हिंदी)...")
        audio = recognizer.listen(source, phrase_time_limit=8)
    try:
        # Try Hindi first
        return recognizer.recognize_google(audio, language="hi-IN")
    except sr.UnknownValueError:
        try:
            # Fallback to English
            return recognizer.recognize_google(audio, language="en-IN")
        except:
            return "माफ़ कीजिए, मैं समझ नहीं पाया।"
    except sr.RequestError:
        return "स्पीच सर्विस उपलब्ध नहीं है।"

# Function: Chat + TTS
def chat_with_ai(user_input):
    instruction = f"आप हमेशा सरल, सहानुभूतिपूर्ण और स्वाभाविक हिंदी में उत्तर दें। उपयोगकर्ता कहता है: {user_input}"
    response = model.generate_content(instruction)
    bot_text = response.text.strip()

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # TTS
    tts = gTTS(bot_text, lang="hi")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    st.audio(tmp_file.name, format="audio/mp3", start_time=0)

# ---- User Input Options ----
col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ बोलें और भेजें"):
        user_input = recognize_speech()
        st.write(f"🗣️ आपने कहा: {user_input}")
        chat_with_ai(user_input)

with col2:
    user_input = st.text_input("✍️ यहाँ लिखें (English या हिंदी)")
    if st.button("Send ✉️") and user_input.strip():
        chat_with_ai(user_input)

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

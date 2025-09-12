import os
import streamlit as st
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import texttospeech

# Load .env file
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

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function: Speak with Google Cloud TTS
def speak_hindi(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-IN",   # Hindi voice
        name="hi-IN-Wavenet-A"   # Natural neural WaveNet voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    with open(tmp_file.name, "wb") as out:
        out.write(response.audio_content)

    st.audio(tmp_file.name)

# Function: Chat with Gemini
def chat_with_ai(user_input):
    user_input_hindi = f"आप हमेशा सरल, स्वाभाविक और सहानुभूतिपूर्ण हिंदी में उत्तर दें। उपयोगकर्ता कहता है: {user_input}"

    response = model.generate_content(user_input_hindi)
    bot_text = response.text.strip()

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # Speak reply
    speak_hindi(bot_text)

# User input
user_input = st.text_input("कैसा महसूस कर रहे हैं? (हिंदी या अंग्रेज़ी में लिखें)")

if st.button("Send") and user_input.strip():
    chat_with_ai(user_input)

# Chat bubble styling
chat_box_style = """
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    width: 60%;
    color: black;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
"""

# Display chat
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

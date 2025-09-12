from google import genai
import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    st.error("API key not found! Please set GOOGLE_GENAI_API_KEY in your .env file.")
    st.stop()

st.set_page_config(page_title="🌸 ManoSakhi - Hindi Mental Health Bot 🌸")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

client = genai.Client(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_ai(user_input):
    # Prepend instruction in Hindi to force model response in Hindi
    user_input_hindi = f"आप हमेशा हिंदी में उत्तर दें। उपयोगकर्ता कहता है: {user_input}"

    conversation = [{"role": "user", "parts": [{"text": user_input_hindi}]}]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=conversation
    )
    bot_text = response.text

    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # Always speak reply
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

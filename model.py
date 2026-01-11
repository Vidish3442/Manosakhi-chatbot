<<<<<<< HEAD
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load key
=======
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import streamlit as st
import google.generativeai as genai  # ✅ Correct import
import os
# Load environment variables
>>>>>>> 04f4007c72b9e2bc981fe203b20396fc15a70bc1
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY missing in .env")
    st.stop()

<<<<<<< HEAD
# OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# UI
st.set_page_config(page_title="🌸 ManoSakhi 🌸")
=======
# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="🌸 ManoSakhi - Hindi Mental Health Bot 🌸")
>>>>>>> 04f4007c72b9e2bc981fe203b20396fc15a70bc1
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_ai(user_input):
<<<<<<< HEAD
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "आप एक सहानुभूतिपूर्ण मानसिक स्वास्थ्य सहायक हैं। "
                    "हमेशा सरल, सकारात्मक और स्वाभाविक हिंदी में उत्तर दें।"
                )
            },
            {"role": "user", "content": user_input}
        ]
    )

    bot_reply = response.choices[0].message.content
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_reply))

user_input = st.text_input("✍️ यहाँ लिखें (English या हिंदी)")

if st.button("Send ✉️") and user_input.strip():
    chat_with_ai(user_input)

for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"🧑 **आप:** {msg}")
    else:
        st.markdown(f"🤖 **ManoSakhi:** {msg}")
=======
    # Force reply in empathetic, natural Hindi + Hinglish
    user_input_hindi = f"""
    आप हमेशा सरल, स्वाभाविक और सहानुभूतिपूर्ण भाषा में उत्तर दें।
    पहले हिंदी (देवनागरी) में लिखें, फिर वही उत्तर Hinglish (English letters में Hindi) में लिखें।
    उपयोगकर्ता कहता है: {user_input}
    """

    response = model.generate_content(user_input_hindi)
    bot_text = response.text.strip()

    # Save chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": bot_text})

    # Speak only the Hindi part (first line)
    hindi_line = bot_text.split("\n")[0]
    tts = gTTS(hindi_line, lang="hi")
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
>>>>>>> 04f4007c72b9e2bc981fe203b20396fc15a70bc1

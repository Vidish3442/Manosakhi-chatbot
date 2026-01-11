import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY missing in .env")
    st.stop()

# OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# UI
st.set_page_config(page_title="🌸 ManoSakhi 🌸")
st.title("🌸 ManoSakhi - Hindi Mental Health Chatbot 🌸")
st.subheader("आपका मानसिक स्वास्थ्य साथी 🤗")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_ai(user_input):
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

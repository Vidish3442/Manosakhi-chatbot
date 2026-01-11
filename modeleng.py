import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ------------------ Load API Key ------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("❌ OPENROUTER_API_KEY not found in .env file")
    st.stop()

# ------------------ OpenRouter Client ------------------
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ------------------ UI ------------------
st.set_page_config(page_title="🌸 ManoSakhi 🌸")
st.title("🌸 ManoSakhi – Mental Health Chatbot 🌸")
st.subheader("Your emotional support companion 🤍")

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Chat Function ------------------
def chat_with_ai(user_input):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a kind, empathetic mental health support chatbot. "
                    "Always respond in clear, supportive, and simple English. "
                    "Do not give medical advice. Encourage healthy coping."
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    bot_reply = response.choices[0].message.content

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_reply))

# ------------------ Input ------------------
user_input = st.text_input("✍️ Type your message here (English only)")

if st.button("Send ✉️") and user_input.strip():
    chat_with_ai(user_input)

# ------------------ Chat Display ------------------
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **ManoSakhi:** {msg}")

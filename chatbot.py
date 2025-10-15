import os
import time
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions as google_exceptions


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"  
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat(history=[])


st.set_page_config(page_title="ChatNova", page_icon="💬", layout="wide")


with st.sidebar:
    st.title("⚙️ About")
    st.markdown(f"**Model:** `{MODEL_NAME}`")
    st.markdown("**Version:** `Stable`")
    st.markdown("---")
    st.markdown("💡 *Built using Google Gemini*")
    st.markdown("📍 Developer: **Shivansh Srivastava**")

st.markdown(
    """
    <style>
    body { background-color: #0e1117; color: #fafafa; font-family: 'Inter', sans-serif; }
    .stTextInput>div>div>input { background-color: #1e1e1e; color: white; border-radius: 10px; }
    .user-bubble {
        background-color: #2e8b57;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
        color: white;
    }
    .bot-bubble {
        background-color: #2b2b2b;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: left;
        color: #e4e4e4;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #333;
        border-radius: 12px;
        background-color: #121212;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 ChatNova")
st.caption("Your personal AI assistant powered by Google Gemini⚡")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def get_gemini_response(question):
    for attempt in range(3): 
        try:
            response = chat.send_message(question, stream=False)
            return response
        except google_exceptions.ServiceUnavailable:
            wait = (attempt + 1) * 3
            st.warning(f"⚠️ Model overloaded. Retrying in {wait}s...")
            time.sleep(wait)
    st.error("❌ Model temporarily unavailable. Try again later.")
    return None

st.markdown("---")
user_input = st.text_input("💭 Ask something:", key="input")
if st.button("🚀 Send"):
    if user_input.strip():
        st.session_state["chat_history"].append(("You", user_input))

        with st.spinner("Just a moment..."):
            response = get_gemini_response(user_input)

        if response:
            full_response = ""
            placeholder = st.empty()

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(
                        f"<div class='bot-bubble'>{full_response}</div>",
                        unsafe_allow_html=True,
                    )

            st.session_state["chat_history"].append(("Gemini", full_response))
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.subheader("🕒 Conversation History")

chat_html = "<div class='chat-container'>"
for role, text in st.session_state["chat_history"]:
    if role == "You":
        chat_html += f"<div class='user-bubble'>{text}</div>"
    else:
        chat_html += f"<div class='bot-bubble'>{text}</div>"
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

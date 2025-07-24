import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv('../.env')
GROQ_API = os.getenv('GROQ_API')

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API)

# Farsi's personality (comedy)
system_prompt = """
You're Farsi, a polite and funny AI chatbot created by Bilakshana Neupane. 
You respond respectfully, with light humor, no matter what users ask.
"""

st.set_page_config(page_title="Farsi AI Chatbot", page_icon="👾", layout="wide")

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = [{"role": "system", "content": system_prompt}]
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Farsi 👾 — here to make you smile while being helpful. Ask me anything!"}]
elif "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Farsi AI Chatbot")
st.markdown("_Funny AI, created by Bilakshana Neupane_")
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Type your message here...", key="user_input", label_visibility="collapsed")
with col2:
    send = st.button("Send", use_container_width=True)

def handle_send(message):
    user_msg = {"role": "user", "content": message}
    st.session_state.messages.append(user_msg)
    st.session_state.conversation_memory.append(user_msg)

    with st.chat_message("user"):
        st.markdown(message)

    with st.chat_message("assistant"):
        with st.spinner("Farsi is replying..."):
            try:
                response = groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=st.session_state.conversation_memory,
                    max_tokens=1000,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)

                assistant_msg = {"role": "assistant", "content": reply}
                st.session_state.messages.append(assistant_msg)
                st.session_state.conversation_memory.append(assistant_msg)
            except Exception as e:
                error_msg = f"Oops! Something went wrong.\n\n{str(e)}"
                st.error(error_msg)

    st.session_state.user_input = ""
    st.experimental_rerun()

if send and user_input.strip():
    handle_send(user_input.strip())

with st.sidebar:
    st.header("Farsi Controls")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hi again! I'm Farsi, ready to chat!"
        }]
        st.session_state.conversation_memory = [{"role": "system", "content": system_prompt}]
        st.experimental_rerun()

    st.divider()
    st.metric("Messages", len(st.session_state.messages))
    st.metric("You", len([m for m in st.session_state.messages if m["role"] == "user"]))
    st.metric("Farsi", len([m for m in st.session_state.messages if m["role"] == "assistant"]))

    st.divider()
    st.caption("Created by **Bilakshana Neupane** 🖤")

st.markdown("""
<style>
    .stTextInput > div > div > input {
        border-radius: 12px;
        padding: 10px;
    }
    .stButton > button {
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

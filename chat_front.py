import streamlit as st
import uuid
from chat_backend import run_chat

st.set_page_config(page_title="LangGraph Chatbot", layout="centered")

st.title("🤖 LangGraph + Perplexity Chatbot")

# -------------------------------------------------------
# Session-safe thread id
# -------------------------------------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# -------------------------------------------------------
# Chat history
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------------
# Input
# -------------------------------------------------------
prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    result = run_chat(prompt, st.session_state.thread_id)

    ai_msg = result["messages"][-1].content

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_msg}
    )

    with st.chat_message("assistant"):
        st.markdown(ai_msg)

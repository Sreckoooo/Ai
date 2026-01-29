import os
from groq import Groq
import streamlit as st
from datetime import datetime

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MAX_MESSAGES = 10

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Si prijazen asistent za Puff Shop Slovenija. Odgovarjaš izključno v slovenščini in samo na vprašanja, povezana z izdelki Puff Shop Slovenija."}
    ]

st.set_page_config(page_title="Puff Shop Slovenija – Chatbot", layout="centered")
st.title("💨 Puff Shop Slovenija – klepetalnik")
st.write("Vprašaj me karkoli o naših izdelkih.")

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

vnos = st.chat_input("Vpiši vprašanje")

if vnos:
    st.session_state.messages.append({"role": "user", "content": vnos})

    try:
        odgovor = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = odgovor.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(ai_text)

        st.session_state.messages.append({"role": "assistant", "content": ai_text})

        if len(st.session_state.messages) > MAX_MESSAGES:
            st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    except Exception as e:
        st.error(f"Prišlo je do napake: {e}")
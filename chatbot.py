import os
from groq import Groq
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Puff Shop Slovenija – Chatbot",
    layout="wide"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MAX_MESSAGES = 10

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Si namenski klepetalnik spletne strani Puff Shop Slovenija. Odgovarjaš izključno v slovenščini. DOVOLJENA so samo vprašanja, ki so neposredno povezana s spletno stranjo Puff Shop Slovenija, njenimi izdelki, ponudbo, uporabo izdelkov in osnovnimi informacijami o trgovini. Če uporabnik postavi vprašanje, ki NI povezano s Puff Shop Slovenija (npr. vreme, matematika, splošna vprašanja, osebne teme), moraš vljudno odgovoriti, da za to nimaš informacij in da lahko pomagaš samo glede Puff Shop Slovenija."}
    ]

st.title("💨 Puff Shop Slovenija – klepetalnik")
st.write("Vprašaj me karkoli o naših izdelkih.")

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

vnos = st.chat_input("Vpiši vprašanje")

if vnos:
    st.session_state.messages.append({"role": "user", "content": vnos})

    dovoljene_besede = [
        "puff", "puff shop", "vape", "okus", "okusi", "nikotin",
        "izdelek", "izdelki", "ponudba", "trgovina", "slovenija",
        "uporaba", "kako uporabljati", "cena", "kupi", "naročilo"
    ]

    if not any(beseda in vnos.lower() for beseda in dovoljene_besede):
        zavrnitev = (
            "Oprosti, na to vprašanje ne morem odgovoriti. "
            "Pomagam lahko samo z informacijami o spletni strani "
            "Puff Shop Slovenija in njenih izdelkih."
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": zavrnitev}
        )

        with st.chat_message("assistant"):
            st.markdown(zavrnitev)

    else:
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
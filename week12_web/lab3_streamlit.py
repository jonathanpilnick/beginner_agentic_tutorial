"""
Week 12 · Day 3 · Lab 3: A Streamlit chat app in a few dozen lines.

The same brain and the same memory.json as Lab 2, with a new face, written only in Python.
  TODO 1  show_history()     the chat so far: st.session_state + st.chat_message
  TODO 2  memory_sidebar()   what the assistant remembers, with a Forget button per fact
  TODO 3  answer()           a new message: st.chat_input -> remember, answer, show

Run:    streamlit run lab3_streamlit.py     (opens http://localhost:8501; stop it with Ctrl+C)
Check:  python check_lab3.py                (runs the app without a browser and names your next step)

Streamlit reruns this whole file from top to bottom every time you click or send something.
st.session_state is the dictionary that survives those reruns.

Your AI tutor: open https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/lab3
copy the prompt and paste it into Claude Code.
"""

import sys
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
sys.path.insert(1, str(ROOT))
from assistant import MEMORY_FILE, chat, extract_facts, load_memory, save_memory  # noqa: E402
from lab2_web import load_settings, persona_for            # noqa: E402  (your Lab 2 settings from .env)

settings = load_settings()
NAME = settings["name"]

st.set_page_config(page_title=f"{NAME} · chat", page_icon="💬")
st.title(f"💬 Chat with {NAME}")
st.caption("Built with Streamlit: the same brain and memory as your Flask app.")


# ---------- TODO 1: show the chat so far --------------------------------------------
def show_history():
    """Create the message list once per browser tab, then draw every message in it."""
    # TODO 1: if "messages" is not in st.session_state yet, set st.session_state.messages = [].
    #   Then for each message m in it, draw it inside `with st.chat_message(m["role"]):`
    #   using st.markdown(m["content"]).
    raise NotImplementedError("TODO 1 in lab3_streamlit.py")


# ---------- TODO 2: the memory, in the sidebar ------------------------------------------
def memory_sidebar():
    """List the saved facts in the sidebar, each with a Forget button."""
    with st.sidebar:
        st.header(f"What {NAME} remembers")
        memory = load_memory(MEMORY_FILE)
        if not memory:
            st.write("Nothing yet. Tell me about yourself!")
        # TODO 2: for each key, value in memory.items(): st.write(f"**{key}**: {value}"), then a
        #   st.button("Forget", key=f"forget_{key}") (every button needs its own key).
        #   When the button returns True (it was just clicked): delete the key, save the memory,
        #   and call st.rerun() so the page is drawn again without it.
        raise NotImplementedError("TODO 2 in lab3_streamlit.py")


# ---------- TODO 3: answer a new message ----------------------------------------------
def answer(prompt):
    """Show the user's message, remember facts, answer with the memory and the history, save both."""
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # TODO 3: the same steps as Lab 2's /api/chat: facts = extract_facts(prompt); load the
            #   memory and save it with the new facts (if any); then
            #   reply = chat(prompt, memory, st.session_state.messages, persona=persona_for(NAME))
            raise NotImplementedError("TODO 3 in lab3_streamlit.py")
        st.markdown(reply)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
    if facts:
        st.rerun()                              # redraw so the sidebar shows the new facts


# ---------- Given: the page, top to bottom ------------------------------------------------
show_history()
memory_sidebar()
if prompt := st.chat_input(f"Message {NAME}"):   # None until the user sends something
    answer(prompt)

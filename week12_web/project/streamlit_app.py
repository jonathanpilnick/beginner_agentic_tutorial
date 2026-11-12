"""
streamlit_app.py - the project starter as a Streamlit app (Python only, no HTML or JavaScript).

It already works with the example feature in feature.py. Make it yours: change feature.py and this page.
Run these from the week12_web folder (so Streamlit finds .streamlit/config.toml):
  streamlit run project/streamlit_app.py      then open http://localhost:8501   (stop with Ctrl+C)
  python project/test_project.py              the tests (no Claude calls)
"""

import sys
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(1, str(HERE.parent))
from feature import EXAMPLE_INPUT, MAX_CHARS, format_result, run_feature   # noqa: E402
from llm import ClaudeCodeError                                            # noqa: E402
from settings import load_settings                                         # noqa: E402

NAME = load_settings()["name"]
st.set_page_config(page_title=NAME, page_icon="✨")
st.title(f"✨ {NAME}")

if "results" not in st.session_state:        # survives Streamlit's reruns, one list per browser tab
    st.session_state.results = []

text = st.text_area("Your input", placeholder=EXAMPLE_INPUT, height=180, max_chars=MAX_CHARS)
if st.button("Run", type="primary"):
    if not text.strip():
        st.warning("Type something first.")
    else:
        try:
            with st.spinner("Thinking..."):
                result = run_feature(text.strip())
            st.session_state.results.insert(0, format_result(result))   # newest first
        except ClaudeCodeError:
            st.error("The AI is unavailable right now. Try again.")

for shown in st.session_state.results:
    with st.container(border=True):
        st.markdown(shown)

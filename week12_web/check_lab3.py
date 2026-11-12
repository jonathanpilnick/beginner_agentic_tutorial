"""
check_lab3.py - run your Streamlit app WITHOUT a browser, and print what the page shows.

It uses Streamlit's own testing tool (AppTest), so you and your tutor can both see the result.
  python check_lab3.py          checks TODO 1 and TODO 2 (no Claude calls)
  python check_lab3.py chat     also sends one chat message, for TODO 3 (2 Claude calls)
"""

import logging
import re
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from assistant import MEMORY_FILE, load_memory, save_memory   # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Hide a harmless warning ("missing ScriptRunContext") that Streamlit prints when an app runs without a browser.
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").addFilter(
    lambda record: "missing ScriptRunContext" not in record.getMessage())

APP = HERE / "lab3_streamlit.py"
TIMEOUT = 180            # seconds per run: a run that calls Claude takes longer than the 3-second default


def problem(at):
    """If the app raised an error, print it (and the next TODO) and return True."""
    if not at.exception:
        return False
    message = at.exception[0].message
    todo = re.search(r"TODO \d+ in \w+\.py", message)
    if "ADMIN_TOKEN" in message:          # Lab 2's settings: .env is missing or has no token
        print(f"\n>>> Setup needed: {message.strip().splitlines()[0]}")
    elif todo:
        print(f"\n>>> Next step: {todo.group(0)}. Finish it, then run this check again.")
    else:
        print("\nThe app raised an error. Read its last line first:\n", message)
    return True


def show_page(at, label):
    print(f"--- {label} ---")
    print("Title:", at.title[0].value if at.title else "(none)")
    for m in at.chat_message:
        text = " ".join(md.value for md in m.markdown)
        print(f"  [{m.name}] {text[:300]}")
    facts = [md.value for md in at.sidebar.markdown]
    print("Sidebar:", " | ".join(facts) if facts else "(empty)")


def main():
    at = AppTest.from_file(str(APP), default_timeout=TIMEOUT).run()
    if at.title:                           # the page as far as it got, even if a TODO stopped it
        show_page(at, "The page, before any message")
    if problem(at):
        return

    # TODO 2: the Forget button deletes a fact (a test fact, so your own memory is safe)
    memory = load_memory(MEMORY_FILE)
    memory["test_fact"] = "delete me"
    save_memory(memory, MEMORY_FILE)
    at = AppTest.from_file(str(APP), default_timeout=TIMEOUT).run()
    if problem(at):
        return
    buttons = [b for b in at.button if b.key == "forget_test_fact"]
    if not buttons:
        print("\nNo Forget button with key 'forget_test_fact' in the sidebar yet (TODO 2: key=f\"forget_{key}\").")
        return
    buttons[0].click().run()
    if problem(at):
        return
    gone = "test_fact" not in load_memory(MEMORY_FILE)
    print("Forget button: " + ("PASS, the fact was deleted from memory.json" if gone else "FAIL, it is still saved"))

    if sys.argv[1:] != ["chat"]:
        print("\nTODO 1 and TODO 2 work. Next: TODO 3, then run:  python check_lab3.py chat")
        return
    message = "Hi! I'm Noa and I play the guitar. Give me one tip for practising."
    print("\nSending:", message)
    at.chat_input[0].set_value(message).run()
    if problem(at):
        return
    show_page(at, "The page, after one message")
    roles = [m.name for m in at.chat_message]
    ok = roles[-2:] == ["user", "assistant"]
    print("Chat: " + ("PASS, your message and the reply are on the page" if ok
                      else "FAIL, expected a user message and an assistant reply"))
    if ok:
        print("\nAll 3 TODOs work. Now open it in the browser:  streamlit run lab3_streamlit.py")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as setup:      # e.g. ADMIN_TOKEN missing in .env (Lab 2, Part 1)
        print(f"\n>>> Setup needed: {setup}")

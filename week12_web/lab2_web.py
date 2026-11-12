"""
Week 12 · Day 2 · Lab 2: A web page for your assistant.

Your Lab 1 API grows into a real web app: settings and a secret from the environment,
a chat that remembers you, memory endpoints protected by a token, and a page in the browser.
  Part 1  load_settings()          config and a secret from environment variables (.env)  (TODO 1)
  Part 2  POST /api/chat           chat with memory: remember facts, answer with the history (TODO 2)
  Part 3  DELETE /api/memory/<key> forget a fact, only with the secret admin token          (TODO 3)
  Part 4  GET /                    the chat page: templates/index.html + static/chat.js      (TODO 4)

Before Part 1: copy .env.example to .env and put a random ADMIN_TOKEN in it (your tutor helps).
Run:  python lab2_web.py          runs every part you have finished (no server needed)
      python lab2_web.py 3        runs only Part 3
      python lab2_web.py serve    starts the web app: open http://127.0.0.1:5001 in your browser

Your AI tutor: open https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/lab2
copy the prompt and paste it into Claude Code.
"""

import os
import secrets
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
sys.path.insert(1, str(ROOT))                             # after this file's own folder
from assistant import MEMORY_FILE, PERSONA, chat, extract_facts, load_memory, save_memory  # noqa: E402
from lab1_api import PORT, get_message                    # noqa: E402  (your Lab 1 request check)
from llm import ClaudeCodeError                            # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Read the .env file into the environment. Variables that are already set win (override=False).
load_dotenv(ROOT / ".env")

app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=str(ROOT / "static"))


# ---------- Part 1: configuration and secrets from the environment ----------------
def load_settings():
    """Read the app's settings from environment variables and return them as a dict."""
    # TODO 1: read ASSISTANT_NAME from os.environ (default "Remy") and ADMIN_TOKEN (default "").
    #   If the token is shorter than 16 characters, raise RuntimeError with a message that says how to
    #   fix it (copy .env.example to .env and put a random token in it).
    #   Return {"name": <the name>, "admin_token": <the token>}.
    raise NotImplementedError("TODO 1 in lab2_web.py")


def persona_for(name):
    """The Week 11 persona, with your assistant's name."""
    return PERSONA.replace("Remy", name)


def clean_history(data):
    """The chat history the page sends: a list of {"role": "user"/"assistant", "content": "..."}.
    Anything else is dropped: never trust what a client sends."""
    history = data.get("history") if isinstance(data, dict) else None
    if not isinstance(history, list):
        return []
    return [m for m in history[-6:] if isinstance(m, dict) and m.get("role") in ("user", "assistant")
            and isinstance(m.get("content"), str)]


@app.errorhandler(ClaudeCodeError)
def assistant_unavailable(error):
    """If any route fails to reach Claude, answer 503 with a short JSON message."""
    return {"error": "The assistant is unavailable right now. Try again."}, 503


# ---------- Part 2: a chat that remembers --------------------------------------------
@app.post("/api/chat")
def chat_endpoint():
    """POST {"message": "...", "history": [...]} -> {"reply": "...", "remembered": {...}}"""
    data = request.get_json(silent=True)
    message, error = get_message(data)          # Lab 1
    if error:
        return {"error": error}, 400
    settings = load_settings()
    history = clean_history(data)
    # TODO 2: the Week 11 memory loop, now behind an endpoint:
    #   1) facts = extract_facts(message). Load the memory (MEMORY_FILE); if there are new facts,
    #      add them (memory.update) and save the memory.
    #   2) reply = chat(message, memory, history, persona=persona_for(settings["name"]))
    #   3) return {"reply": reply, "remembered": facts}
    raise NotImplementedError("TODO 2 in lab2_web.py")


# ---------- Part 3: memory endpoints -------------------------------------------------
@app.get("/api/memory")
def get_memory():
    """Everyone may see the memory (it's your own laptop). Deleting needs the token."""
    return {"memory": load_memory(MEMORY_FILE)}


@app.delete("/api/memory/<key>")
def forget(key):
    """DELETE /api/memory/<key> with the header X-Admin-Token: <your token> -> {"deleted": key}"""
    settings = load_settings()
    sent = request.headers.get("X-Admin-Token", "")
    # TODO 3: 1) if `sent` doesn't match settings["admin_token"], return {"error": "Wrong or missing X-Admin-Token"}
    #      with status 401. Compare with secrets.compare_digest(sent.encode(), <token>.encode()), not ==.
    #   2) load the memory; if `key` isn't in it, return {"error": f"No fact called {key!r}"} with 404.
    #   3) delete the key, save the memory, and return {"deleted": key}.
    raise NotImplementedError("TODO 3 in lab2_web.py")


# ---------- Part 4: the chat page ----------------------------------------------------
@app.get("/")
def index():
    """The web page. Flask fills {{ name }} in templates/index.html; static/chat.js does the chatting."""
    # TODO 4: return render_template("index.html", ...) with name= your assistant's name from load_settings().
    #   Then open templates/index.html and find {{ name }}.
    raise NotImplementedError("TODO 4 in lab2_web.py")


# ---------- the demo: run the parts you have finished ----------------------------------
def make_client():
    app.testing = True    # show errors from your code here, instead of a bare "500 Internal Server Error"
    return app.test_client()


def part1():
    print("=== Part 1 · Settings and a secret from the environment ===")
    settings = load_settings()
    print("Assistant name:", settings["name"])
    print(f"Admin token loaded: yes, {len(settings['admin_token'])} characters (never print a secret itself)")
    print()


def part2():
    print("=== Part 2 · A chat that remembers ===")
    client = make_client()
    first = "Hi, I'm Noa. I'm vegetarian and I love live jazz."
    r = client.post("/api/chat", json={"message": first, "history": []})
    body = r.get_json()
    print("You :", first)
    print(" ->", r.status_code, "remembered", body.get("remembered"))
    print("Bot :", body.get("reply"))
    history = [{"role": "user", "content": first}, {"role": "assistant", "content": body.get("reply", "")}]
    second = "What should I cook tonight?"
    r = client.post("/api/chat", json={"message": second, "history": history})
    print("You :", second)
    print(" ->", r.status_code, "remembered", r.get_json().get("remembered"))
    print("Bot :", r.get_json().get("reply"))
    print()


def part3():
    print("=== Part 3 · Memory endpoints and a secret token ===")
    client = make_client()
    token = load_settings()["admin_token"]       # first, so an unfinished TODO 1 leaves memory.json alone
    memory = load_memory(MEMORY_FILE)
    memory["test_fact"] = "delete me"
    save_memory(memory, MEMORY_FILE)
    print("GET /api/memory ->", client.get("/api/memory").get_json())
    for label, headers in (("no token", {}), ("wrong token", {"X-Admin-Token": "guess123"}),
                           ("the right token", {"X-Admin-Token": token})):
        r = client.delete("/api/memory/test_fact", headers=headers)
        print(f"DELETE /api/memory/test_fact with {label:15} ->", r.status_code, r.get_json())
    r = client.delete("/api/memory/test_fact", headers={"X-Admin-Token": token})
    print(f"{'DELETE /api/memory/test_fact again':49} ->", r.status_code, r.get_json())
    print()


def part4():
    print("=== Part 4 · The chat page ===")
    client = make_client()
    r = client.get("/")
    html = r.get_data(as_text=True)
    title = html.split("<title>")[1].split("</title>")[0] if "<title>" in html else "?"
    print("GET / ->", r.status_code, f"an HTML page of {len(html)} characters, titled '{title}'")
    print("GET /static/chat.js ->", client.get("/static/chat.js").status_code)
    print(f"Now start the app (python lab2_web.py serve) and open http://127.0.0.1:{PORT}\n")


if __name__ == "__main__":
    if sys.argv[1:] == ["serve"]:
        app.run(host="127.0.0.1", port=PORT, debug=True)
        sys.exit()
    chosen = sys.argv[1:] or ["1", "2", "3", "4"]
    try:
        for number, part in (("1", part1), ("2", part2), ("3", part3), ("4", part4)):
            if number in chosen:
                part()
        if len(chosen) == 4:
            print("All 4 parts work. Start it with: python lab2_web.py serve")
    except NotImplementedError as todo:
        print(f"\n>>> Next step: {todo}. Finish it, then run the file again.")
    except RuntimeError as problem:
        print(f"\n>>> Setup needed: {problem}")

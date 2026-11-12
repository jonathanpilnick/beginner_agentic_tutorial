"""
Week 12 · Day 1 · Lab 1: Your agent gets an API.

Last week your assistant lived in a terminal. Today it gets a web API, so any program
(a web page, a phone app, another agent) can talk to it over HTTP.
  Part 1  GET  /api/health   your first JSON route                                (TODO 1, 1 line)
  Part 2  POST /api/chat     check the request (TODO 2), then answer with Claude (TODO 3)
  Part 3  call_api()         a Python client that calls your running server       (TODO 4)

Run:  python lab1_api.py          runs every part you have finished (Parts 1-2 need no server)
      python lab1_api.py 2        runs only Part 2
      python lab1_api.py serve    starts the real server at http://127.0.0.1:5001 (keep it running)

Your AI tutor: open https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/lab1
copy the prompt and paste it into Claude Code.
"""

import sys
from pathlib import Path

import requests
from flask import Flask, request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
sys.path.insert(1, str(ROOT))                             # after this file's own folder
from assistant import chat                                 # noqa: E402  (the brain from Week 11)
from llm import ClaudeCodeError                            # noqa: E402

# Print any character (Hebrew, emoji) even where the console isn't UTF-8 (Windows).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PORT = 5001                        # not 5000: on a Mac, AirPlay Receiver often uses port 5000
BASE_URL = f"http://127.0.0.1:{PORT}"
MAX_CHARS = 2000                   # longer messages are refused: they cost more and can be abuse

app = Flask(__name__)


@app.get("/")
def home():
    """A plain-text page, so the browser shows something at http://127.0.0.1:5001/"""
    return "Hello from Flask! Your assistant's API is at /api/health and /api/chat."


# ---------- Part 1: your first JSON route --------------------------------------
@app.get("/api/health")
def health():
    """Tell callers the server is up. Flask turns a returned dict into a JSON response."""
    # TODO 1: return a dict with "status": "ok" and "assistant": "Remy".
    #   That's all: Flask turns the dict into JSON and sends status 200 (OK).
    raise NotImplementedError("TODO 1 in lab1_api.py")


# ---------- Part 2: an endpoint that serves AI ---------------------------------
def get_message(data):
    """Check the JSON body of a chat request. Return (message, None) if it is good,
    or (None, "what is wrong") if not. `data` is the parsed JSON (None if it wasn't JSON)."""
    # TODO 2: never trust what a client sends. Return (None, 'Send JSON like {"message": "Hi"}') when
    #   data isn't a dict, or data.get("message") isn't a string, or it is empty after .strip().
    #   Return (None, f"Message too long (max {MAX_CHARS} characters)") when it is longer than MAX_CHARS.
    #   Otherwise return (the stripped message, None).
    raise NotImplementedError("TODO 2 in lab1_api.py")


@app.post("/api/chat")
def chat_endpoint():
    """POST {"message": "..."} -> {"reply": "..."}"""
    message, error = get_message(request.get_json(silent=True))
    if error:
        return {"error": error}, 400          # 400 Bad Request: the client sent something wrong
    # TODO 3: get the answer with chat(message) (from assistant.py) and return {"reply": <the answer>}.
    #   If chat() raises ClaudeCodeError (not logged in, usage limit...), return
    #   {"error": "The assistant is unavailable right now. Try again."} with status 503 instead.
    raise NotImplementedError("TODO 3 in lab1_api.py")


# ---------- Part 3: a client for your API ----------------------------------------
def call_api(message, base_url=BASE_URL):
    """Send `message` to the running server's /api/chat and return the reply text."""
    # TODO 4: send it with requests.post() to f"{base_url}/api/chat", with json={"message": message}
    #   and timeout=120 (Week 4!). If the status code isn't 200, raise RuntimeError with the code and
    #   the "error" from the JSON body. Otherwise return the "reply" from the JSON body.
    raise NotImplementedError("TODO 4 in lab1_api.py")


# ---------- the demo: run the parts you have finished ----------------------------
def make_client():
    """Flask's test client sends requests to the app without a real server."""
    app.testing = True    # show errors from your code here, instead of a bare "500 Internal Server Error"
    return app.test_client()


def part1():
    print("=== Part 1 · Your first JSON route ===")
    client = make_client()
    r = client.get("/api/health")
    print("GET /api/health ->", r.status_code, r.get_json())
    print()


def part2():
    print("=== Part 2 · An endpoint that serves AI ===")
    client = make_client()
    r = client.post("/api/chat", json={})
    print("POST /api/chat with {}            ->", r.status_code, r.get_json())
    r = client.post("/api/chat", data="hello", content_type="text/plain")
    print("POST /api/chat with plain text    ->", r.status_code, r.get_json())
    r = client.post("/api/chat", json={"message": "x" * (MAX_CHARS + 1)})
    print(f"POST /api/chat with {MAX_CHARS + 1} chars    ->", r.status_code, r.get_json())
    message = "Hi! In one sentence: what is a web API?"
    r = client.post("/api/chat", json={"message": message})
    print(f'POST /api/chat {{"message": "{message}"}}')
    print("  ->", r.status_code, r.get_json())
    print()


def part3():
    print("=== Part 3 · Call your running server from another program ===")
    try:
        reply = call_api("Hi from a Python client! Reply in one short sentence.")
    except requests.exceptions.ConnectionError:
        print(f"No server is running at {BASE_URL}.")
        print("Open a SECOND terminal in this folder, activate .venv, run:  python lab1_api.py serve")
        print("then come back to this terminal and run:  python lab1_api.py 3")
        return False
    print(f"POST {BASE_URL}/api/chat over real HTTP")
    print("Reply:", reply)
    print("Look at the server's terminal: it printed one line for this request.\n")
    return True


if __name__ == "__main__":
    # python lab1_api.py        runs every part you have finished
    # python lab1_api.py 2      runs only Part 2
    # python lab1_api.py serve  starts the server (stop it with Ctrl+C)
    if sys.argv[1:] == ["serve"]:
        app.run(host="127.0.0.1", port=PORT, debug=True)
        sys.exit()
    chosen = sys.argv[1:] or ["1", "2", "3"]
    try:
        ok = True
        for number, part in (("1", part1), ("2", part2), ("3", part3)):
            if number in chosen:
                ok = part() is not False and ok
        if len(chosen) == 3 and ok:
            print("All 3 parts work. Your agent has an API: any program can now talk to it over HTTP.")
    except NotImplementedError as todo:
        print(f"\n>>> Next step: {todo}. Finish it, then run the file again.")

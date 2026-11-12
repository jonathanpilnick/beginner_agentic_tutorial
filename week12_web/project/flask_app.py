"""
flask_app.py - the project starter with a Flask backend and an HTML/JavaScript page.

It already works with the example feature in feature.py. Make it yours:
change feature.py, the page (templates/project.html and static/project.js), and the routes if you need more.
  GET  /             the page
  GET  /api/health   {"status": "ok"}
  POST /api/run      {"text": "..."} -> {"result": {...}, "text": "markdown to show"}
  GET  /api/stats    how many times the feature ran; needs the header X-Admin-Token (your .env secret)

Run these from the week12_web folder:
  python project/flask_app.py          then open http://127.0.0.1:5002   (stop with Ctrl+C)
  python project/test_project.py       the tests (no Claude calls)
"""

import secrets
import sys
from pathlib import Path

from flask import Flask, render_template, request

HERE = Path(__file__).resolve().parent
sys.path.insert(1, str(HERE.parent))
from feature import EXAMPLE_INPUT, MAX_CHARS, format_result, run_feature   # noqa: E402
from llm import ClaudeCodeError                                            # noqa: E402
from settings import load_settings                                         # noqa: E402

PORT = 5002                 # Lab 1 and Lab 2 use 5001, so both can run at the same time
app = Flask(__name__)
stats = {"runs": 0}         # kept in memory: it starts again at 0 when the server restarts


def get_text(data):
    """Check the request body. Return (text, None) or (None, "what is wrong")."""
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return None, 'Send JSON like {"text": "your input"}'
    if len(data["text"]) > MAX_CHARS:
        return None, f"Too long (max {MAX_CHARS} characters)"
    return data["text"].strip(), None


@app.get("/")
def index():
    return render_template("project.html", name=load_settings()["name"], example=EXAMPLE_INPUT)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/run")
def run():
    text, error = get_text(request.get_json(silent=True))
    if error:
        return {"error": error}, 400
    try:
        result = run_feature(text)
    except ClaudeCodeError:
        return {"error": "The AI is unavailable right now. Try again."}, 503
    stats["runs"] += 1
    return {"result": result, "text": format_result(result)}


@app.get("/api/stats")
def get_stats():
    token = load_settings()["admin_token"]
    sent = request.headers.get("X-Admin-Token", "")
    if len(token) < 16 or not secrets.compare_digest(sent.encode(), token.encode()):
        return {"error": "Wrong or missing X-Admin-Token"}, 401
    return stats


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)

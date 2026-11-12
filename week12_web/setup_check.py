"""
setup_check.py - run this first (Week 12 Lab 1, Part 0):   python setup_check.py

Checks Python, the Python packages (Flask, Streamlit, python-dotenv, requests),
that Python can talk to Claude through your Claude Code login, and that the lab ports are free.
"""

import json
import os
import platform
import shutil
import socket
import subprocess
import sys
from importlib.metadata import version

OK, WARN, FAIL = "[ OK ]", "[WARN]", "[FAIL]"
problems = 0

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1. Python version: the kit supports 3.11-3.15 (Streamlit 1.67 needs 3.11 or newer).
#    On a Mac, Streamlit needs pyarrow, whose builds need macOS 12 or newer (checked November 2026).
v = sys.version_info
mac = platform.mac_ver()[0] if sys.platform == "darwin" else ""
mac_major = int(mac.split(".")[0]) if mac else 0
if not (3, 11) <= v < (3, 16):
    problems += 1
    print(FAIL, f"Python {v.major}.{v.minor} found. Install Python 3.13 from python.org")
elif mac and mac_major < 12:
    problems += 1
    print(FAIL, f"macOS {mac}: Streamlit needs macOS 12 or newer. Pair with a neighbour.")
else:
    print(OK, f"Python {v.major}.{v.minor}.{v.micro}")

# 2. Packages
for name, module in (("flask", "flask"), ("streamlit", "streamlit"), ("python-dotenv", "dotenv"),
                     ("requests", "requests")):
    try:
        __import__(module)
        print(OK, f"{name} {version(name)}")
    except ImportError:
        problems += 1
        print(FAIL, f"{name} missing. Run:  pip install -r requirements.txt")

# 3. Claude Code
claude = shutil.which("claude")
if not claude:
    problems += 1
    print(FAIL, "`claude` not found. Open a new terminal; see https://code.claude.com/docs/en/setup")
else:
    out = subprocess.run([claude, "--version"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    print(OK, f"Claude Code {out.stdout.strip()}")
    status = subprocess.run([claude, "auth", "status"], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    try:
        info = json.loads(status.stdout)
        if info.get("loggedIn"):
            print(OK, f"Logged in (auth method: {info.get('authMethod')})")
        else:
            problems += 1
            print(FAIL, "Not logged in. Run `claude` once in a terminal and log in.")
    except json.JSONDecodeError:
        print(WARN, "Could not read `claude auth status`. Run `claude update`.")

if os.environ.get("ANTHROPIC_API_KEY"):
    print(WARN, "ANTHROPIC_API_KEY is set. llm.py ignores it, but Claude Code itself (your tutor chat) "
                "may bill that API key instead of your plan. Remove it from your environment.")

# 4. The ports the labs use: 5001 (Flask labs), 5002 (Flask project), 8501 (Streamlit)
for port, used_by in ((5001, "Lab 1 and Lab 2"), (5002, "the Flask project"), (8501, "Streamlit")):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            print(OK, f"Port {port} is free ({used_by})")
        except OSError:
            print(WARN, f"Port {port} is in use ({used_by} needs it). A lab server you left running? "
                        "Stop it with Ctrl+C in its terminal.")

# 5. End-to-end call
if claude and problems == 0:
    try:
        from llm import ask_claude_json
        reply = ask_claude_json("Reply with status 'web lab ready'.",
                                {"type": "object", "properties": {"status": {"type": "string"}}, "required": ["status"]})
        print(OK, f"Claude replied with JSON: {reply}")
    except Exception as e:  # noqa: BLE001 - show any error to the student
        problems += 1
        print(FAIL, f"Calling Claude failed: {e}")

print("\nAll good - you're ready for Week 12!" if problems == 0
      else f"\n{problems} problem(s) found - fix the [FAIL] lines above.")

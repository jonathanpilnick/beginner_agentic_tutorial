"""
Learn it with your AI tutor: in Claude Code, type
  Be my tutor for Week 10 Lab 0. Read tutor/lab0_setup.md completely and follow it.

setup_check.py - run this first:   python setup_check.py

Checks Python, the Python packages, the free local embedding model,
and that Python can talk to Claude through your Claude Code login.
"""

import json
import os
import shutil
import subprocess
import sys

OK, WARN, FAIL = "[ OK ]", "[WARN]", "[FAIL]"
problems = 0

# 1. Python version: the kit supports 3.11-3.14. onnxruntime (used by Chroma's embedder)
#    had no Python 3.15 build when this kit was made (October 2026).
v = sys.version_info
if (3, 11) <= v < (3, 15):
    print(OK, f"Python {v.major}.{v.minor}.{v.micro}")
else:
    problems += 1
    print(FAIL, f"Python {v.major}.{v.minor} found. Install Python 3.13 (or 3.12) from python.org")

# 2. Packages
for name in ("chromadb", "numpy", "pypdf"):
    try:
        mod = __import__(name)
        print(OK, f"{name} {getattr(mod, '__version__', '')}")
    except ImportError:
        problems += 1
        print(FAIL, f"{name} missing. Run:  pip install -r requirements.txt")

# 3. Embedding model (downloads under 100 MB the first time, then works offline)
try:
    from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
    vec = DefaultEmbeddingFunction()(["hello world"])[0]
    print(OK, f"Embedding model works: 'hello world' -> {len(vec)} numbers")
except Exception as e:  # noqa: BLE001 - show any error to the student
    problems += 1
    print(FAIL, f"Embedding model failed: {e}")

# 4. Claude Code
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
    print(WARN, "ANTHROPIC_API_KEY is set. llm.py ignores it so your subscription is used.")

# 5. End-to-end call
if claude and problems == 0:
    try:
        from llm import ask_claude
        reply = ask_claude("Reply with exactly three words: RAG pipeline ready")
        print(OK, f"Claude replied: {reply}")
    except Exception as e:  # noqa: BLE001
        problems += 1
        print(FAIL, f"Calling Claude failed: {e}")

print("\nAll good - you're ready for Week 10!" if problems == 0
      else f"\n{problems} problem(s) found - fix the [FAIL] lines above.")

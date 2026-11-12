# Week 12: Web Interfaces with Flask & Streamlit - student kit

Your assistant from Week 11 lived in a terminal. This week it gets a web interface: an API, a web page,
a Streamlit app, and then a web AI app of your own choice.

| When | What you build | File |
|---|---|---|
| Day 1 · Lab 1 | **Your agent gets an API**: Flask routes, JSON, status codes, an endpoint that serves AI, a Python client | `lab1_api.py` |
| Day 2 · Lab 2 | **A web page for your assistant**: settings and a secret from `.env`, a chat that remembers, a protected route, an HTML/JavaScript page | `lab2_web.py`, `templates/`, `static/` |
| Day 3 · Lab 3 | **The same assistant in Streamlit**: chat in a few dozen lines of Python, `st.session_state`, a memory sidebar | `lab3_streamlit.py`, `check_lab3.py` |
| Day 4 · Project | **Ship it**: a web AI app of your own choice, built with Flask or Streamlit, tested and demoed | `project/`, `PROJECT_BRIEF.md` |

Each lab reuses the code you wrote in the one before it.

## Learn with your AI tutor (recommended)

Every lab has a page with a prompt you paste into **Claude Code**. Claude becomes your private tutor:
it explains what you'll build and why, teaches the ideas in short steps, and guides you while **you**
write the code.

- Lab pages: https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/index.html
- Or, inside this folder, run `claude` and type: `Be my tutor for Week 12 Lab 1. Read tutor/lab1_api.md completely and follow it.`

## What runs where

Everything runs on your own computer with **free, open-source** packages.
The only account you need is your **Claude Code** login. No API keys, no purchases, no hosting account.

| Part | What runs it | Cost |
|---|---|---|
| Web server and API | Flask's development server at `http://127.0.0.1:5001` (the project uses `5002`) | free |
| Streamlit apps | `streamlit run ...` at `http://localhost:8501` | free |
| The assistant's brain | `assistant.py` from Week 11; Claude through `claude -p` (Claude Code's non-interactive mode), see `llm.py` | your Claude plan's usage limits |
| Settings and secrets | `.env` (your copy of `.env.example`), read with python-dotenv | free |

Both servers only accept connections from your own computer (`127.0.0.1` / `localhost`).
`.env` holds your secret token and `memory.json` holds facts about you, so both are in `.gitignore`.

## Setup (Lab 1, Part 0)

Your tutor walks you through this. To do it yourself:

1. Python **3.13** from python.org (on Windows, tick "Add python.exe to PATH").
   - Works on Python 3.11 to 3.15. Macs need macOS 12 or newer (Streamlit's pyarrow package, checked November 2026).
   - Wrong version on Windows? `py install 3.13`, then use `py -3.13 -m venv .venv` in step 2.
2. Open a terminal **in this folder** (not inside OneDrive or another synced folder) and create a virtual environment:

   Windows (PowerShell):
   ```powershell
   py -3.13 -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
   In the old Command Prompt (cmd.exe), activate with `.venv\Scripts\activate.bat`.

   macOS / Linux (on a Mac, `python3` can be Apple's old 3.9, so name the version):
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   Linux without `python3.13` (Ubuntu 24.04 ships 3.12): if `python3 --version` says 3.11 or newer, use
   `python3 -m venv .venv`. If it is older (Ubuntu 22.04 ships 3.10), install Python 3.13 first, from your
   distribution's packages or the deadsnakes PPA on Ubuntu.
3. Check Claude Code: `claude --version`, then `claude update` if it is old (the labs need the `--json-schema` option).
4. Run `python setup_check.py`. Every line should say `[ OK ]`.

You'll make your `.env` file in Lab 2, Part 1.

## Running two things at once

A web server keeps running until you stop it, so it needs its own terminal:

- **Terminal 1:** the server, for example `python lab1_api.py serve` (stop it with **Ctrl+C**).
- **Terminal 2:** everything else, for example `python lab1_api.py 3` or `claude`.

Activate `.venv` in every new terminal. Don't start a server with `!` inside Claude Code: it never finishes.

## Files

| File | What it is |
|---|---|
| `lab1_api.py` | Lab 1: 3 parts, 4 small TODOs |
| `lab2_web.py` | Lab 2: 4 parts, 4 small TODOs (uses your Lab 1 `get_message()`) |
| `templates/index.html`, `static/chat.js` | Lab 2's web page: HTML with a Jinja `{{ name }}`, and the JavaScript that calls your API |
| `lab3_streamlit.py`, `check_lab3.py` | Lab 3: 3 small TODOs, and a checker that runs the app without a browser |
| `project/` | Day 4: a working starter app (Flask **and** Streamlit versions), `feature.py` (your AI feature), tests and `check_project.py` |
| `PROJECT_BRIEF.md` | Day 4: the brief, idea menu and grading |
| `assistant.py` | The Week 11 brain: memory, fact extraction, chat. Nothing to do in it |
| `llm.py` | `ask_claude()`, `ask_claude_json()` and `stream_claude()`: call Claude through your Claude Code login |
| `.env.example` | The settings your apps read. Copy it to `.env` (Lab 2) |
| `.streamlit/config.toml` | Streamlit settings: only your computer can open the app; no usage statistics |
| `setup_check.py` | Checks Python, the packages, Claude Code and the ports |
| `data/sample_notes.md` | Sample study notes for the project starter |
| `tutor/` | The tutor guides Claude Code reads |
| `solutions/` | Reference solutions for the labs. Try first! |

## Troubleshooting

- **`ModuleNotFoundError`:** your virtual environment isn't active. Activate it (step 2) and run again.
  Still failing? Run the environment's Python directly: `.venv\Scripts\python` (Windows) or `.venv/bin/python`.
- **Linux: "ensurepip is not available":** install the venv package (`sudo apt install python3-venv`), then repeat step 2.
- **`claude` is not recognized:** open a *new* terminal after installing Claude Code. See https://code.claude.com/docs/en/setup
- **"Address already in use" or "Port 5001 is in use":** a server is still running in another terminal. Stop it with Ctrl+C there.
- **`No server is running at http://127.0.0.1:5001`:** start it in a second terminal: `python lab1_api.py serve`.
- **A "403" from `http://127.0.0.1:5000`:** on a Mac, AirPlay Receiver may use port 5000. The labs use 5001: open `http://127.0.0.1:5001`.
- **`>>> Setup needed: ADMIN_TOKEN is missing or too short`:** copy `.env.example` to `.env` and put a token in it (Lab 2, Part 1).
- **The page loads but nothing happens when you send:** open the browser's developer tools (F12), Console tab, and read the error.
- **Changed `chat.js` but the page didn't change:** reload with Ctrl+Shift+R (Cmd+Shift+R on a Mac).
- **Your Lab 1 code has a bug and Lab 2 needs it:** copy `solutions/lab1_api.py` over `lab1_api.py` (same for Lab 2 and Lab 3).
- **Start over with an empty memory:** delete `memory.json`.
- **Windows on ARM laptops:** install the x64 ("AMD64") Python 3.13 from python.org; Windows 11 runs it under emulation.
- **You hit a usage limit:** wait for the reset. Run one part at a time, for example `python lab2_web.py 3`.

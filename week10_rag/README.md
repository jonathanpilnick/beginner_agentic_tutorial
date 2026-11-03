# Week 10: Retrieval-Augmented Generation (RAG) - student kit

In two days you build a RAG system from scratch, then use it
on **your own** documents:

| When | What you build | File |
|---|---|---|
| Day 1 · Lab 1 | **Search your documents by meaning**: embeddings, chunking, a ChromaDB index, search | `lab1_search.py` |
| Day 2 · Lab 2 | **Answer with sources**: put the best chunks in a prompt, Claude answers and cites them | `lab2_answer.py` |
| Day 2 · Final project | **Ask My Docs**: a Q&A bot over your own files, tested, reviewed by a peer, demoed | `qa_bot.py`, `PROJECT_BRIEF.md` |

Each step reuses the code you wrote in the one before it.

## Learn with your AI tutor (recommended)

Every lab has a page with a prompt you paste into **Claude Code**. Claude becomes your private tutor:
it explains what you'll build and why, teaches the ideas in short steps, and guides you while **you**
write the code.

- Lab pages: https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/index.html
- Or, inside this folder, run `claude` and type: `Be my tutor for Week 10 Lab 1. Read tutor/lab1_search.md completely and follow it.`

## What runs where

Everything runs on your own computer with **free, open-source** packages.
The only account you need is your **Claude Code** login. No API keys, no purchases.

| Step | What runs it | Cost |
|---|---|---|
| Embeddings | `all-MiniLM-L6-v2`, run locally by ChromaDB (under 100 MB, downloaded once) | free |
| Vector database | ChromaDB, running inside your Python program | free |
| Generation | Claude, through `claude -p` (Claude Code's non-interactive mode), see `llm.py` | your Claude plan's usage limits |

## Setup (Lab 1, Part 0)

Your tutor walks you through this. To do it yourself:

1. Python **3.13** from python.org. On Windows, tick "Add python.exe to PATH".
   - The kit works on Python 3.11-3.13 everywhere, and on 3.14 except on Intel Macs and macOS 13.
     It does **not** work on 3.15 yet: onnxruntime, which ChromaDB needs, had no 3.15 build in October 2026.
   - Macs need macOS 13 or newer. macOS's built-in `python3` is too old, so install 3.13 from python.org.
   - Wrong version on Windows? With the `py` launcher: `py install 3.13`, then use `py -3.13 -m venv .venv` in step 2.
   - Linux with Python 3.10 or older (e.g. Ubuntu 22.04): install the free tool uv, then `uv python install 3.13`.
2. Open a terminal **in this folder** and create a virtual environment. Keep the folder out of OneDrive
   (or any synced folder): syncing locks the `.venv` and `chroma_db` files.

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If PowerShell says running scripts is disabled, run this once and retry:
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
   (In the old Command Prompt, cmd.exe, activate with `.venv\Scripts\activate.bat` instead.)

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Check Claude Code: `claude --version`, then `claude update` if it is old.
4. Run `python setup_check.py`. Every line should say `[ OK ]`.

## Files

| File | What it is |
|---|---|
| `lab1_search.py` | Lab 1: 3 parts, 4 small TODOs |
| `lab2_answer.py` | Lab 2: 3 parts, 3 small TODOs (uses your Lab 1 `search()`) |
| `qa_bot.py` + `PROJECT_BRIEF.md` | Final project: 2 TODOs, then test, README, peer review, demo |
| `evaluate.py` | Tests retrieval with questions you know the answer to (hit@3). No Claude calls |
| `llm.py` | `ask_claude(prompt, system=...)`: calls Claude through your Claude Code login |
| `setup_check.py` | Checks Python, the packages, the embedding model and Claude Code |
| `data/handbook/` | A **fictional** company handbook used in the labs; `data/handbook_questions.json` has 16 test questions |
| `tutor/` | The tutor guides Claude Code reads |
| `solutions/` | Reference solutions. Try first! |

## Troubleshooting

- **`ModuleNotFoundError`:** your virtual environment isn't active. Activate it (step 2) and run again.
- **`claude` is not recognized:** open a *new* terminal after installing Claude Code. See https://code.claude.com/docs/en/setup
- **The embedding model download fails:** it is fetched once, from `chroma-onnx-models.s3.amazonaws.com`. Retry on a
  stable connection; on a school or company network, ask whether that site is blocked.
- **`pip install` fails on onnxruntime:** your Python or macOS version has no onnxruntime build (Python 3.15; Python 3.14
  on an Intel Mac or macOS 13; macOS 12 or older). Install Python 3.13 and recreate `.venv`.
- **Your Lab 1 code has a bug and Lab 2 needs it:** copy `solutions/lab1_search.py` over `lab1_search.py` (the solutions work from either folder).
- **`qa_bot.py` seems to freeze inside Claude Code:** it waits for you to type. Run it in a normal terminal, not with `!`.
- **Windows on ARM laptops (e.g. Snapdragon):** ChromaDB publishes Windows packages for x64 only. Install the x64
  ("AMD64") Python 3.13 from python.org: Windows 11 runs it under emulation and pip then installs the x64 packages.
  If that fails, pair with a neighbour.
- **You hit a usage limit:** wait for the limit to reset and ask fewer test questions. `evaluate.py` never uses Claude.

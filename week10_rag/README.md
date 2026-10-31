# Week 10: Retrieval-Augmented Generation (RAG) - student kit

Aardvark AI developer program, Week 10. Over three lessons you build a RAG system from scratch:
embeddings, then a vector database, then chunking and evaluation, then cited answers from Claude.
It ends with a Q&A bot over **your own** documents.

## Learn with your AI tutor (recommended)

Every lab has a tutor guide for **Claude Code** in [`tutor/`](tutor/README.md). Claude becomes your
private tutor: it explains what you'll build and why it matters, asks how you like to learn,
then walks you through the lab step by step while **you** write the code.

1. **Get the kit:** `git clone https://github.com/jonathanpilnick/beginner_agentic_tutorial.git`, or click **Code → Download ZIP** on GitHub and unzip it. Then open a terminal in `beginner_agentic_tutorial/week10_rag`.
2. **Run `claude`** in that folder.
3. **Paste:** `Be my tutor for Week 10 Lab 0. Read tutor/lab0_setup.md completely and follow it.`

Lab 0 sets everything up with your tutor. The start lines for every lab are in [`tutor/README.md`](tutor/README.md).

## What runs where

Everything runs on your own computer with **free, open-source** packages.
The only account you need is your **Claude Code** login. No API keys, no purchases.

| Step | What runs it | Cost |
|---|---|---|
| Embeddings | `all-MiniLM-L6-v2`, run locally by ChromaDB (under 100 MB, downloaded once) | free |
| Vector database | ChromaDB, running inside your Python program | free |
| Generation | Claude, through `claude -p` (Claude Code's non-interactive mode), see `llm.py` | your Claude plan's usage limits |

## Manual setup (if you prefer to set up without the tutor)

1. Python **3.13** (or 3.12) from python.org. The kit works on 3.11-3.14, **not 3.15**: onnxruntime, which ChromaDB
   needs, had no Python 3.15 build in October 2026. On Windows, tick "Add python.exe to PATH".
   Already on 3.15? Versions can live side by side. With the Windows `py` launcher:
   `py install 3.13`, then create the environment with `py -3.13 -m venv .venv` in step 2.
2. Open a terminal **in this folder** and create a virtual environment:

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If PowerShell says running scripts is disabled, run this once and retry:
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Check Claude Code: `claude --version`, then `claude update` if it is old.
4. Run `python setup_check.py`. Every line should say `[ OK ]`.

## Files

| File | Lesson | What you do |
|---|---|---|
| `tutor/` | all | Tutor guides for Claude Code, one per lab ([start here](tutor/README.md)) |
| `setup_check.py` | 1 | Lab 0: checks Python, packages, the embedding model and Claude Code |
| `lab1_embeddings.py` | 1 | Embed sentences, cosine similarity, search without a database |
| `lab2_chroma_basics.py` | 2 | Chroma: add, query, filter, update, delete, persist |
| `lab3_ingest.py` | 2 | Load .txt/.md/.pdf, chunk with overlap, store with metadata |
| `lab4_retrieval_eval.py` | 2 | Measure hit@1, hit@3 and MRR for different chunk sizes |
| `lab5_rag_answer.py` | 3 | Build a grounded prompt and generate a cited answer with Claude |
| `qa_bot.py` + `PROJECT_BRIEF.md` | 3 | Project: Q&A bot over your own documents |
| `llm.py` | all | `ask_claude(prompt, system=...)` helper |
| `data/handbook/` | 2-3 | A **fictional** company handbook used in the labs |
| `solutions/` | - | Reference solutions. Try first! |

## Troubleshooting

- **`claude` is not recognized:** open a *new* terminal after installing Claude Code. See https://code.claude.com/docs/en/setup
- **The embedding model download fails:** it is fetched from the internet the first time only. Retry on a stable connection.
- **`pip install` fails on onnxruntime:** you're probably on Python 3.15. Install 3.13 and recreate `.venv`.
- **Lab 2 shows L2-style distances after you added cosine:** the collection already existed. Delete the `chroma_db` folder and re-run.
- **`ModuleNotFoundError`:** your virtual environment isn't active. Activate it (step 2) and run again.
- **Weird characters when reading files on Windows:** always open text with `encoding="utf-8"`.
- **Chroma says the collection name is invalid:** names need 3-512 characters from `a-z A-Z 0-9 . _ -`.
- **Windows on ARM laptops:** ChromaDB publishes Windows wheels for x64 only. Ask the instructor.
- **You hit a usage limit:** wait for the limit to reset, use fewer test questions, and keep `haiku` as the model in `llm.py`.

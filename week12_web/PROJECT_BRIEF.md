# Week 12 project: Ship it

Build a **web AI app of your own choice** and ship it on Day 4: a real interface, a backend that
handles errors, settings and secrets kept out of the code, tests, and a demo.

You choose the idea. It must use an AI feature that connects to what you learned in the course
(prompts and structured output, tools, retrieval from Week 10, memory from Week 11...) and a web
interface from this week (Flask or Streamlit). It's a portfolio piece, and it can grow into your capstone
(Weeks 13 to 16).

**When:** Day 4. A 15-minute idea pitch, about 2 hours 15 minutes of building and testing, 20 minutes of peer review, then demos.
**Your AI mentor:** https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/project

## 1. Choose your idea (before the pitch)

Pick one from the menu, change one, or bring your own:

| Idea | The AI part | Builds on |
|---|---|---|
| **Flashcards and quiz** | Notes in, flashcards out; then it quizzes you and checks your answer | structured output (the starter does the first half) |
| **Remember Me on the web** | Your Week 11 assistant with a web page, a memory panel and a Forget button | Week 11 memory, Labs 2 and 3 |
| **Ask my notes** | Paste or pick a few notes; it finds the most relevant one and answers only from it, naming the source | Week 10 retrieval |
| **Fridge chef** | Ingredients in, a recipe out (as JSON: title, steps, time), remembering your diet | structured output, memory |
| **Job ad decoder** | Paste a job ad; get the skills it asks for, what they mean, and 3 interview questions to practise | structured output |
| **Language buddy** | Write in English or Hebrew; it corrects you, explains one mistake and replies | prompts, chat history |
| **Your own idea** | Anything else that fits the rules below | tell us at the pitch |

**Rules:** free only (your Claude Code login through `llm.py`; no API keys, no paid services),
runs on your laptop, and safe to demo (no real personal data: see the privacy rule).

**Idea pitch (15 minutes, in groups of 4):** in 1 minute each, say who it's for, what it does, which
course idea it uses, and Flask or Streamlit. Your group asks one question each. Your instructor OKs ideas.

## 2. Start from the starter

`project/` holds a working app you can change: a **Flashcard Maker**. Try it first, from the `week12_web` folder:

```
python project/feature.py                 # the AI feature alone (1 Claude call)
python project/flask_app.py               # Flask version: open http://127.0.0.1:5002
streamlit run project/streamlit_app.py    # Streamlit version: opens http://localhost:8501
python project/test_project.py            # the tests (no Claude calls)
```

Then make it yours:

1. **`project/feature.py`**: your AI feature. Change `SYSTEM`, `SCHEMA`, `run_feature()` and `format_result()`.
   Both apps only call those two functions.
2. **Choose your interface:** Flask (`flask_app.py` + `templates/project.html` + `static/project.js`) or
   Streamlit (`streamlit_app.py`). You may build both, but one done well is worth more.
3. **Settings:** set `APP_NAME` in `.env`. If your app needs another setting or secret, read it with
   `os.environ` in `project/settings.py` and add it (with an empty or example value) to `.env.example`.
4. **Errors:** bad input gets a clear message (400 in Flask); the AI being down gets 503 or `st.error`.

**Privacy rule:** test with made-up or harmless data. No passwords, ID numbers, health records or other
people's details. Everything you type is sent to Claude, and anything your app saves stays on your laptop.

## 3. Test it

1. `python project/test_project.py`: keep the starter's tests passing as you change it (update a test
   if your idea changes what it checks), and write **at least 2 tests of your own** in `MyTests`.
2. Try 3 inputs of your own in the browser and write down what happened.
3. Find one failure (a wrong or weird answer, a crash, an input it should refuse) and explain why.
   Try one fix and test again.
4. Run `python project/check_project.py`. It should end with `6/6 checks pass`.

## 4. Write `project/PROJECT_README.md`

A new file in the `project` folder (keep the kit's `README.md`). Use these headings, because `check_project.py` looks for them:

```markdown
# <your app's name>
## What it does
One or two sentences: who it's for and what it does.
## Course idea
Which course idea the AI part uses (structured output, retrieval, memory...) and how.
## How to run
The commands, and the settings it needs in .env.
## Tests
What test_project.py checks (including your 2 tests), and your 3 inputs with what happened.
## One failure
What went wrong, why, and what you changed.
```

## 5. Peer review (20 minutes, in pairs)

Swap laptops with a partner. Use their app and fill in this checklist for them:

- [ ] I ran it from the README's commands, and it worked end to end (input, AI answer on the page).
- [ ] I sent empty input and very long input (in Streamlit, the box stops at the limit and shows a counter): I got a clear message or limit, not a crash.
- [ ] `python project/check_project.py` passes on their laptop.
- [ ] My partner searched their `project` folder for the first characters of their token (they type it, not me), and for "token" and "key": nothing outside `.env`.
- [ ] Their code: one thing that is clear, one suggestion to make it better.

## 6. Demo (3 minutes, in groups of 4)

Show: the idea in one sentence, the app working with a live input, one thing in the code you're proud of,
the failure you found and what you learned. Two volunteers then demo to the whole class.

## Grading (100 points)

| Part | Points |
|---|---|
| Works end to end: input in the browser, AI answer on the page | 20 |
| The AI feature: your own idea, using a course idea well | 15 |
| Interface: clear, usable, shows a "thinking" state | 10 |
| Backend and errors: input checked (400 or a message), AI down handled (503 or `st.error`) | 10 |
| Settings and secrets: from `.env`, `.env.example` shared, no secret in the code (`check_project.py`) | 10 |
| Tests: `test_project.py` passes, with at least 2 tests of your own | 10 |
| `PROJECT_README.md` with one failure explained | 5 |
| Peer review: a filled-in checklist for your partner | 10 |
| Demo | 10 |

You may use Claude Code as a pair programmer, but you must be able to explain every line you hand in.

## Stretch goals (optional, pick one)

- **Streaming:** show the answer while Claude writes it. In Streamlit:
  `st.write_stream(stream_claude(prompt, system=SYSTEM))` (from `llm.py`).
- **History:** keep the last 5 results and show them in a sidebar (Streamlit) or a list (Flask).
- **Both faces:** build the Flask and the Streamlit version, and say in your README which you'd ship and why.
- **Deployment plan:** write in your README how you would put it online (what would have to change for
  the AI calls, the secrets and the port). You'll deploy for real in Week 15.

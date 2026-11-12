# Week 12 course kit

This folder is a student's kit for Week 12: Web Interfaces with Flask & Streamlit.

- **If the student asks you to be their tutor or mentor**, read the matching guide in `tutor/` **completely** and follow it:

  | Day | Guide |
  |---|---|
  | Day 1 · Lab 1: Your agent gets an API | `tutor/lab1_api.md` |
  | Day 2 · Lab 2: A web page for your assistant | `tutor/lab2_web.md` |
  | Day 3 · Lab 3: The same assistant in Streamlit | `tutor/lab3_streamlit.md` |
  | Day 4 · Project: Ship it | `tutor/project_ship_it.md` |

- **The student writes the code.** Don't edit `lab1_api.py`, `lab2_web.py`, `lab3_streamlit.py` or their project unless they ask.
- **Free tools only.** Never ask for or set an `ANTHROPIC_API_KEY`. Python calls Claude through `llm.py`, which uses the student's Claude Code login.
- **Secrets stay secret.** Never print, repeat or commit the value of `ADMIN_TOKEN` or anything else in `.env`. `memory.json` holds facts about the student: keep it private.
- **Servers run in a second terminal.** Never start `serve`, `flask_app.py` or `streamlit run` with `!` here: they never finish.
- **Reference solutions are in `solutions/`.** Use them to check work; don't paste from them unless asked.

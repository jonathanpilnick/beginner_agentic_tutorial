# Learn every lab with your own AI tutor

Every Week 10 lab comes with a tutor guide written for **Claude Code**. Claude reads the guide and becomes your private tutor:
- It tells you what you'll build, and why it's useful and cool.
- It asks how you like to learn.
- It walks you through the lab step by step.

You write the code. Claude explains, reviews, gives hints and quizzes you.

## Start a lab in 3 steps

1. **Open a terminal in the `week10_rag` folder.**
2. **Activate the course environment.** Skip this for Lab 0, which creates it.
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
3. **Start Claude Code** with `claude`, and paste the line for your lab:

| Lab | Paste this into Claude Code |
|---|---|
| 0 · Setup | `Be my tutor for Week 10 Lab 0. Read tutor/lab0_setup.md completely and follow it.` |
| 1 · Embeddings | `Be my tutor for Week 10 Lab 1. Read tutor/lab1_embeddings.md completely and follow it.` |
| 2 · ChromaDB | `Be my tutor for Week 10 Lab 2. Read tutor/lab2_chromadb.md completely and follow it.` |
| 3 · Ingestion | `Be my tutor for Week 10 Lab 3. Read tutor/lab3_ingestion.md completely and follow it.` |
| 4 · Evaluation | `Be my tutor for Week 10 Lab 4. Read tutor/lab4_evaluation.md completely and follow it.` |
| 5 · Generation | `Be my tutor for Week 10 Lab 5. Read tutor/lab5_generation.md completely and follow it.` |
| Project | `Be my mentor for the Week 10 project. Read tutor/project_qa_bot.md completely and follow it.` |

Tip: inside this folder, Claude Code already knows about the tutor guides (see `CLAUDE.md`), so "Be my tutor for Lab 2" also works.

## Starting from the lab web pages

Each lab has a page with a ready-to-copy prompt: https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/
Open the page your instructor gives you, copy the prompt, and paste it into Claude Code. For Lab 0 you don't need the kit yet: the tutor helps you download it.

## How you and your tutor work together

- **Run code inside the chat** by starting a line with `!`, for example `! python lab1_embeddings.py`. Claude sees the output and reacts to it.
- **Steer your tutor any time** with **hint**, **show me**, **why?**, **slower**, **faster**, **quiz me** or **skip**.
- **Your tutor won't edit your files** unless you ask. Learning happens when you type the code.
- **Your tutor remembers you.** In Lab 0 it saves your learning preferences to `tutor/learner_profile.md`: pace, language, interests. Later labs read that file. (That's an AI agent with external memory, which is next week's topic.)
- **Explanations in Hebrew?** Just say so. Code stays in English.

## Good to know

- **It's free:** everything uses free open-source packages and your Claude Code plan. Never set an `ANTHROPIC_API_KEY`.
- **Lab 5 and the project call Claude from Python,** which counts toward your plan's usage limits. Test with a few questions, not hundreds.
- **Programs that wait for typed input,** like the project chat, run in a second terminal. `!` can't type into them.

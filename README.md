# Beginner Agentic Tutorial

Hands-on AI developer labs where **Claude Code is your private tutor**.

Each lab includes a tutor guide written for Claude Code. Claude reads it and then teaches you step by step:
- It explains what you're building and why it matters.
- It adapts to your pace, your language (English or Hebrew) and your interests.
- **You** write the code; Claude guides, reviews and quizzes you.

**What you need:** a computer and a Claude plan that includes Claude Code (for example Pro or Max). Everything else is free and open source. No API keys.

## Weeks

| Week | Topic | Start here |
|---|---|---|
| 10 | Retrieval-Augmented Generation (RAG): Day 1 Lab 1 search your documents, Day 2 Lab 2 answer with sources, and a final project: a Q&A bot over your own documents | [week10_rag](week10_rag/README.md) |
| 11 | Memory, State & Multi-Step Agents: Lab 1 give your assistant a memory, Lab 2 a planning agent with state and episodic memory, and a project: an assistant that remembers you across sessions | [week11_memory](week11_memory/README.md) |
| 12 | Web Interfaces with Flask & Streamlit: Day 1 Lab 1 a Flask API for your assistant, Day 2 Lab 2 a web page with settings and secrets, Day 3 Lab 3 the same assistant in Streamlit, and Day 4 a project: a web AI app of your own choice | [week12_web](week12_web/README.md) |

## Start a lab

Open your lab's page, copy the prompt, and paste it into Claude Code:
- Week 10: **https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/index.html**
- Week 11: **https://jonathanpilnick.github.io/beginner_agentic_tutorial/week11/index.html**
- Week 12: **https://jonathanpilnick.github.io/beginner_agentic_tutorial/week12/index.html**

## Or start from the kit

1. **Get the repo:** `git clone https://github.com/jonathanpilnick/beginner_agentic_tutorial.git`, or **Code → Download ZIP**.
2. **Open a terminal** in that week's folder (for example `beginner_agentic_tutorial/week11_memory`, or `beginner_agentic_tutorial-main/week11_memory` from the ZIP) and run `claude`.
3. **Paste:** `Be my tutor for Week 11 Lab 1. Read tutor/lab1_memory.md completely and follow it.`

All start lines are in each kit's `tutor/README.md` ([Week 10](week10_rag/tutor/README.md), [Week 11](week11_memory/tutor/README.md), [Week 12](week12_web/tutor/README.md)).

## For AI tutors

Agents can read each guide as plain Markdown. See [llms.txt](llms.txt) for the raw links.

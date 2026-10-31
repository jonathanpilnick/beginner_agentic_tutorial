# Week 10 Project: a Q&A bot over your own documents

**Time:** Lesson 3, about 2 hours, plus a 3-minute demo.
**You need:** your computer, Python, and your Claude Code login. Everything else is free.
**Mentor:** in Claude Code, type `Be my mentor for the Week 10 project. Read tutor/project_qa_bot.md completely and follow it.`

## 1. Choose your documents (10 min)

Collect **5 to 30 files** (.txt, .md or .pdf) into a folder such as `my_docs/`. Good choices:

- Your own notes and READMEs from Weeks 1-9 of this course
- Official documentation pages or Wikipedia articles saved from your browser (Print, then Save as PDF)
- A public-domain book from Project Gutenberg (gutenberg.org, free .txt downloads)

**Privacy rule:** the chunks you retrieve are sent to Claude. Do **not** use passwords, ID numbers,
medical or bank documents, or anyone else's private messages.

**Language:** the default embedding model (all-MiniLM-L6-v2) was trained on English. Hebrew
documents will retrieve poorly; see stretch goal S4.

## 2. Must-have features (MVP, 80 points)

| # | Feature | Points |
|---|---|---|
| M1 | `python qa_bot.py ingest <folder>` loads .txt/.md/.pdf, chunks them with overlap, and stores them in Chroma with `source` and `page` metadata | 15 |
| M2 | `python qa_bot.py chat` answers questions in a loop until `/quit` | 10 |
| M3 | Answers use **only** the retrieved chunks and cite sources like `[notes.md]` or `[guide.pdf p.3]` | 15 |
| M4 | Questions that the documents can't answer get "I couldn't find that in your documents" instead of a made-up answer | 10 |
| M5 | `/sources` prints the chunks (source, distance, first 120 characters) used for the last answer | 10 |
| M6 | An evaluation file with **8 questions** about your documents and the expected source; report your hit@3 (reuse Lab 4) | 10 |
| M7 | `README.md`: what documents you used, how to run the bot, your chunk size and k, your hit@3, one failure you found and why it happened | 10 |

## 3. Demo (20 points)

3 minutes: one question that works, one that the documents can't answer, `/sources`, and the
most interesting failure you found. You must be able to explain any line of your code.

## 4. Stretch goals (bonus, pick any)

- **S1 Follow-up questions:** keep the last 3 turns in the prompt, and add the previous question to the search query so follow-ups like "and what about abroad?" retrieve well.
- **S2 Relevance threshold:** skip chunks whose cosine distance is above a cut-off you measured.
- **S3 Hybrid search:** add keyword search with the free `rank-bm25` package and combine it with vector search. Does hit@3 improve on your questions?
- **S4 Hebrew / multilingual:** use a free multilingual embedding model through `sentence-transformers` (for example `intfloat/multilingual-e5-small`, which expects `query: ` and `passage: ` prefixes). Note: this installs PyTorch, a large download.
- **S5 Word files:** support .docx with the free `python-docx` package.
- **S6 Contextual chunk headers:** prefix each chunk with its file name and heading before embedding. Measure the change in hit@3.
- **S7 Framework version:** rebuild the bot with LangChain or LlamaIndex from Week 9 and compare.

## 5. Rules

- Do not set or use an `ANTHROPIC_API_KEY`. `llm.py` uses your Claude Code subscription.
- Calls to Claude count toward your plan's usage limits: test with a handful of questions.
- Claude Code may help you write code. You are graded on understanding it.

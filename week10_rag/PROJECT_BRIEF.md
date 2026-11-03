# Week 10 final project: Ask My Docs

Build a Q&A bot that answers questions about **your own documents**, shows where each answer came from,
and says so when the answer isn't there. It is the RAG pipeline from Lab 1 and Lab 2, pointed at your files.

It is also a portfolio piece: you can show it to employers, and you will grow it in later weeks
(memory in Week 11, a web interface in Week 12, and possibly your capstone).

**When:** Day 2, after Lab 2. About 75 minutes of building, 15 minutes of peer review, then demos.
**Your AI mentor:** https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/project

## 1. Choose your documents (bring them to Day 2)

- 5 to 20 files: `.txt`, `.md` or `.pdf` (PDFs need real text; scanned pages have none).
- **English** works best: the free embedding model was trained mainly on English.
- Good choices: your own notes from Weeks 1-9, READMEs of your earlier projects, official docs saved as PDF
  from the browser, public-domain books from Project Gutenberg.
- **Privacy rule:** no passwords, IDs, medical or bank files, or other people's messages. Retrieved
  chunks are sent to Claude as part of the prompt.
- Put them in a folder called `my_docs` inside `week10_rag`.

## 2. Build it: `qa_bot.py` (2 TODOs)

1. **Index** your folder: `build_index(folder, collection="my_docs")` from Lab 1.
2. **Chat loop:** read a question with `input()`, call `answer()` from Lab 2, print the reply and its
   sources, stop on `quit`.

Run it in a normal terminal (it waits for you to type): `python qa_bot.py`

## 3. Test it

1. Write `my_questions.json` (in `week10_rag`, with your editor or Claude): 5 questions about your documents,
   each with the file that answers it. Use different words from the documents, the way a real user would ask.
   ```json
   [
     {"question": "Where should I keep my API key?", "source": "week4_notes.md"}
   ]
   ```
2. Run `python evaluate.py my_questions.json my_docs` and write down your **hit@3** (how many of the
   5 found the right file in the top 3). It makes no Claude calls.
3. Ask your bot 2 questions your documents **can't** answer. It should say
   "I don't know based on the documents."
4. Find one failure (a MISS, a wrong answer or a bad citation) and work out why. Try a fix
   (different words, a different `chunk_text` size) and run `evaluate.py` again.

## 4. Write `PROJECT_README.md`

A new file in `week10_rag` (keep the kit's `README.md`). If you later publish the bot as its own GitHub repo,
this becomes that repo's `README.md`.

```markdown
# Ask My Docs: <your topic>
What it does: one or two sentences.
My documents: what they are, how many files.
How to run: the commands.
Test results: hit@3 = ?/5. Two questions it answered well, one it correctly refused.
One failure: what went wrong, why, and what I tried.
```

## 5. Peer review (15 minutes, in pairs)

Swap laptops with a partner. Run their bot and fill in this checklist for them:

- [ ] I asked 3 questions about their documents. Each answer cited a source. The source was the right file.
- [ ] I asked 1 question their documents can't answer. The bot said it didn't know.
- [ ] `python evaluate.py my_questions.json my_docs` gives the same hit@3 as their `PROJECT_README.md`.
- [ ] Their code: one thing that is clear, one suggestion to make it better.

## 6. Demo (3 minutes)

Show: one good answer with its source, one honest "I don't know", your hit@3, and the failure you found
with what you learned from it.

## Grading (100 points)

| Part | Points |
|---|---|
| Works on your documents: indexes your folder, chat loop until `quit` | 20 |
| Answers cite their sources | 20 |
| Says it doesn't know when the answer isn't in your documents | 15 |
| Test: 5 questions in `my_questions.json` and your hit@3 | 15 |
| `PROJECT_README.md` with test results and one failure explained | 10 |
| Peer review: a filled-in checklist for your partner | 10 |
| Demo | 10 |

You may use Claude Code as a pair programmer, but you must be able to explain every line you hand in.

## Stretch goals (optional, pick one)

- **Follow-up questions (a preview of Week 11 memory):** remember the previous question and search with
  both, so "and for interns?" works after "How many vacation days do I get?".
- **Save Claude calls:** print the best `score` for questions your documents answer and for ones they
  don't. Pick a cut-off between them; below it, reply "I couldn't find that" without calling Claude.
- **Make it an agent tool (Weeks 7-8):** give your agent a `search_docs(query)` tool that calls `search()`,
  so the agent decides when to look something up.

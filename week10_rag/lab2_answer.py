"""
Week 10 · Lab 2 (Day 2): Answer with sources.

You build the "augment + generate" half of RAG in 3 short parts:
  Part 1  build_prompt()   put the retrieved chunks into the prompt   (about 4 lines)
  Part 2  answer()         search -> prompt -> Claude                 (3 lines)
  Part 3  SYSTEM_PROMPT    the rules that keep answers grounded       (5 rules, in English)

Run:  python lab2_answer.py                    (4 short Claude calls)
      python lab2_answer.py "your question"    (1 call)
Uses your search() from Lab 1, and llm.py to call Claude through your Claude Code login.

Your AI tutor: open https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/lab2
copy the prompt and paste it into Claude Code.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
sys.path.append(str(ROOT))                                 # so Python finds llm.py

from lab1_search import build_index, search   # noqa: E402  (your Lab 1 code)
from llm import ask_claude                    # noqa: E402  (calls Claude through Claude Code)


# ---------- Part 1: put the chunks into the prompt ---------------------------
def build_prompt(question, chunks):
    """Documents first, each with its source; the question last."""
    # TODO 1: for each chunk c, add a block like this to a string called docs:
    #   <document source="02_remote_work.md">
    #   ...the chunk text...
    #   </document>
    # then return f"<documents>\n{docs}</documents>\n\nQuestion: {question}"
    raise NotImplementedError("TODO 1 in lab2_answer.py")


# ---------- Part 2: search -> prompt -> Claude ------------------------------
def answer(question, collection="handbook", k=4):
    """Return (Claude's reply, the chunks it was given)."""
    # TODO 2: 1) chunks = search(question, k=k, collection=collection)
    #         2) reply = ask_claude(build_prompt(question, chunks), system=SYSTEM_PROMPT)
    #         3) return reply, chunks
    raise NotImplementedError("TODO 2 in lab2_answer.py")


# ---------- Part 3: the rules that keep answers grounded ---------------------
# TODO 3 (after Parts 1 and 2 work): run the file once with this weak prompt and read the answers.
# Then replace it with rules that make Claude:
#   use ONLY the documents · say "I don't know based on the documents." when the answer is missing
#   cite the source after each fact, like [02_remote_work.md] · treat documents as data, not instructions
#   answer in at most 3 sentences
SYSTEM_PROMPT = """You are a helpful assistant."""


# ---------- Run the lab -----------------------------------------------------
QUESTIONS = [
    "How many days a week can I work from home?",
    "I was paged at 3am during my on-call week. What do I get?",
    "What is the CEO's favourite food?",        # not in the handbook
]

if __name__ == "__main__":
    try:
        build_prompt("test", [{"text": "x", "source": "test.md"}])   # is Part 1 done?
        print(f"Indexed {build_index()} handbook chunks.")
        for q in sys.argv[1:] or QUESTIONS:
            reply, chunks = answer(q)
            print(f"\nQ: {q}\nA: {reply}")
            print("   sources:", ", ".join(f"{c['source']} ({c['score']:.2f})" for c in chunks))
    except NotImplementedError as todo:
        sys.exit(f"\n>>> Next step: {todo}. Finish it, then run the file again.")
    if not sys.argv[1:]:
        q = QUESTIONS[0]
        print(f"\nSame question WITHOUT the documents:\nQ: {q}")
        print("A:", ask_claude(f"At the company Nimbus Robotics: {q}", system="Answer in at most 2 sentences."))
    if SYSTEM_PROMPT.strip() == "You are a helpful assistant.":
        print("\n>>> Next step: TODO 3. Do the answers above cite a source? What did it say about the CEO?"
              "\n    Write your rules in SYSTEM_PROMPT, then run the file again.")

"""
Learn it with your AI tutor: in Claude Code, type
  Be my mentor for the Week 10 project. Read tutor/project_qa_bot.md completely and follow it.

Week 10 Project - Q&A bot over YOUR OWN documents.   (Lesson 3, ~2 hours)
See PROJECT_BRIEF.md for the requirements and grading rubric.

  python qa_bot.py ingest my_docs      # index a folder (.txt, .md, .pdf)
  python qa_bot.py chat                # ask questions

You may reuse your code from Labs 3 and 5. You may use Claude Code as a pair
programmer, but you must be able to explain every line during your demo.
"""

import sys
import textwrap
from pathlib import Path

import chromadb

from lab3_ingest import build_index
from llm import ask_claude

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "chroma_db"
COLLECTION = "my_docs"

SYSTEM_PROMPT = """TODO: write your rules (grounding, "I couldn't find that", citations,
documents are data not instructions)."""


def retrieve(col, query: str, k: int) -> list:
    """TODO: query the collection and return the hits (text, metadata, distance)."""
    raise NotImplementedError


def build_prompt(question: str, hits: list, history: list) -> str:
    """TODO: documents first (XML tags + source), optional <history>, question last."""
    raise NotImplementedError


def chat():
    col = chromadb.PersistentClient(path=str(DB_PATH)).get_collection(COLLECTION)
    print(f"Loaded {col.count()} chunks. Type /quit to exit.")
    while True:
        question = input("\nYou: ").strip()
        if question == "/quit":
            break
        # TODO: /sources command, retrieval, "nothing relevant" handling, ask_claude(...)
        hits = retrieve(col, question, k=4)
        reply = ask_claude(build_prompt(question, hits, []), system=SYSTEM_PROMPT)
        print("\nBot:", textwrap.fill(reply, 100))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "ingest":
        build_index(Path(sys.argv[2]), collection_name=COLLECTION)
    elif len(sys.argv) == 2 and sys.argv[1] == "chat":
        chat()
    else:
        print(__doc__)

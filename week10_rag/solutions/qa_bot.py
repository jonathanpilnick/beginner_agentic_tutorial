"""
Week 10 · Final project · SOLUTION: Ask My Docs, a Q&A bot over your own documents.

Run in a normal terminal (it waits for you to type):
  python solutions/qa_bot.py               (indexes my_docs/)
  python solutions/qa_bot.py path/to/folder
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE
sys.path.append(str(ROOT))

from lab1_search import build_index   # noqa: E402  (Lab 1)
from lab2_answer import answer        # noqa: E402  (Lab 2)

COLLECTION = "my_docs"


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "my_docs"
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}. Put 5-20 of your .txt, .md or .pdf files in it.")

    # Part 1: index your documents (into their own collection, so the handbook stays separate)
    n = build_index(folder, collection=COLLECTION)
    print(f"Indexed {n} chunks from {folder}. Ask a question, or type quit.")

    # Part 2: the chat loop
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("", "quit", "exit"):
            break
        reply, chunks = answer(question, collection=COLLECTION)
        print("Bot:", reply)
        print("Sources:", ", ".join(dict.fromkeys(c["source"] for c in chunks)))


if __name__ == "__main__":
    main()

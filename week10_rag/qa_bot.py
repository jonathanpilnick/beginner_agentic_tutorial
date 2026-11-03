"""
Week 10 · Final project: Ask My Docs, a Q&A bot over your own documents.

It reuses your Lab 1 (build_index, search) and Lab 2 (answer) code. Two TODOs:
  Part 1  index the documents in your my_docs folder
  Part 2  a chat loop: question -> answer() -> print the reply and its sources

Run in a normal terminal (it waits for you to type):
  python qa_bot.py               (indexes my_docs/)
  python qa_bot.py path/to/folder
The full brief: PROJECT_BRIEF.md. Your AI mentor:
https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/project
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
    # TODO 1: n = build_index(folder, collection=COLLECTION)
    #         then print how many chunks were indexed, and "Ask a question, or type quit."


    # Part 2: the chat loop
    # TODO 2: repeat forever:
    #   question = input("\nYou: ").strip()
    #   stop (break) if the question is empty, "quit" or "exit"
    #   reply, chunks = answer(question, collection=COLLECTION)
    #   print the reply, then the sources (each file once): ", ".join(dict.fromkeys(c["source"] for c in chunks))
    print("TODO 1 and TODO 2 in qa_bot.py are next.")


if __name__ == "__main__":
    main()

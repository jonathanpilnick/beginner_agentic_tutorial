"""
evaluate.py - test your retrieval with questions you already know the answer to.

Run:  python evaluate.py                                (the handbook, 16 questions)
      python evaluate.py my_questions.json my_docs      (your project: questions file, documents folder)

The questions file is a list like:
  [{"question": "How many vacation days do new employees get?", "source": "03_vacation_and_leave.md"}, ...]
"source" is the file that holds the answer (for a PDF just the file name, any page counts).

It indexes the folder, then for each question searches the top 3 chunks and checks whether
the right file is among them. hit@3 = the share of questions where it is.
No Claude calls, so it's free and fast: change chunk_text() settings and run it again.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE))
from lab1_search import HANDBOOK, build_index, search  # noqa: E402  (your Lab 1 code)


def evaluate(questions_file, folder, k=3):
    collection = "handbook" if Path(folder).resolve() == HANDBOOK.resolve() else "my_docs"
    print(f"Indexed {build_index(folder, collection=collection)} chunks from {folder}\n")
    questions = json.loads(Path(questions_file).read_text(encoding="utf-8-sig"))  # -sig: also reads files saved with a BOM
    hits = 0
    for q in questions:
        sources = [r["source"] for r in search(q["question"], k=k, collection=collection)]
        hit = any(s == q["source"] or s.startswith(q["source"] + " p.") for s in sources)
        hits += hit
        print(f"{'HIT ' if hit else 'MISS'}  {q['question']}")
        if not hit:
            print(f"      expected {q['source']}, got {sources}")
    print(f"\nhit@{k}: {hits}/{len(questions)} = {hits / len(questions):.2f}")


if __name__ == "__main__":
    questions_file = sys.argv[1] if len(sys.argv) > 1 else HERE / "data" / "handbook_questions.json"
    folder = sys.argv[2] if len(sys.argv) > 2 else HANDBOOK
    evaluate(questions_file, folder)

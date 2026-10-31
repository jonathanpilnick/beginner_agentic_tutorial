"""
Learn it with your AI tutor: in Claude Code, type
  Be my tutor for Week 10 Lab 4. Read tutor/lab4_evaluation.md completely and follow it.

Lab 4 - Measure retrieval quality before you add an LLM.      (Lesson 2, ~35 min)
Run:  python lab4_retrieval_eval.py        (needs a working lab3_ingest.py)

Metrics (higher is better):
  hit@1  - share of questions whose correct source is the #1 result
  hit@3  - share of questions whose correct source is in the top 3
  MRR    - mean reciprocal rank: average of 1/rank of the first correct result
           (0 if it isn't in the top 5)
"""

import json
from pathlib import Path

import chromadb

from lab3_ingest import DEFAULT_FOLDER, build_index

ROOT = Path(__file__).resolve().parent
QUESTIONS = json.loads((ROOT / "data" / "eval_questions.json").read_text(encoding="utf-8"))
CONFIGS = [(150, 0), (300, 50), (600, 100), (1200, 200), (3000, 300)]   # (chunk_size, overlap)


def evaluate(col, k: int = 5) -> dict:
    hit1 = hit3 = rr = 0.0
    for q in QUESTIONS:
        res = col.query(query_texts=[q["question"]], n_results=k,
                        where={"archived": False})          # ignore archived policies
        sources = [m["source"] for m in res["metadatas"][0]]
        # TODO: if q["source"] is in sources:
        #           rank = its position + 1
        #           add 1/rank to rr; add 1 to hit1 if rank == 1; add 1 to hit3 if rank <= 3
    n = len(QUESTIONS)
    return {"hit@1": hit1 / n, "hit@3": hit3 / n, "MRR": rr / n}


if __name__ == "__main__":
    client = chromadb.EphemeralClient()                     # in memory: nothing saved
    print(f"{len(QUESTIONS)} test questions\n")
    print(f"{'chunk':>6} {'overlap':>8} {'#chunks':>8} {'hit@1':>6} {'hit@3':>6} {'MRR':>6}")
    for size, overlap in CONFIGS:
        col = build_index(DEFAULT_FOLDER, size, overlap, client=client,
                          collection_name=f"eval_{size}_{overlap}", verbose=False)
        m = evaluate(col)
        print(f"{size:>6} {overlap:>8} {col.count():>8} {m['hit@1']:>6.2f} {m['hit@3']:>6.2f} {m['MRR']:>6.2f}")

# TASKS
# T1. Which configuration wins? Is the difference big?
# T2. Find the questions that fail (print them!). Why did retrieval miss? Would keyword
#     search (BM25) have found them?
# T3. Add 4 questions of your own to data/eval_questions.json and re-run.
# T4. With only 16 questions, how much should you trust a 0.06 difference?

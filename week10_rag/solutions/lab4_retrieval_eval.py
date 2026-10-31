"""
Lab 4 (SOLUTION) - Measure retrieval quality before you add an LLM.
Run:  python solutions/lab4_retrieval_eval.py

Metrics (higher is better):
  hit@1  - share of questions whose correct source is the #1 result
  hit@3  - share of questions whose correct source is in the top 3
  MRR    - mean reciprocal rank: 1/rank of the first correct result (0 if not in the top 5)
"""

import json
from pathlib import Path

import chromadb

from lab3_ingest import DEFAULT_FOLDER, build_index

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # also works if copied to the main folder
QUESTIONS = json.loads((ROOT / "data" / "eval_questions.json").read_text(encoding="utf-8"))
CONFIGS = [(150, 0), (300, 50), (600, 100), (1200, 200), (3000, 300)]   # (chunk_size, overlap)


def evaluate(col, k: int = 5) -> dict:
    hit1 = hit3 = rr = 0.0
    for q in QUESTIONS:
        res = col.query(query_texts=[q["question"]], n_results=k,
                        where={"archived": False})          # ignore archived policies
        sources = [m["source"] for m in res["metadatas"][0]]
        if q["source"] in sources:
            rank = sources.index(q["source"]) + 1
            rr += 1 / rank
            hit1 += rank == 1
            hit3 += rank <= 3
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

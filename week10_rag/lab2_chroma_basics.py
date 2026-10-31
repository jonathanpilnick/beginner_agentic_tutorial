"""
Learn it with your AI tutor: in Claude Code, type
  Be my tutor for Week 10 Lab 2. Read tutor/lab2_chromadb.md completely and follow it.

Lab 2 - ChromaDB basics: store, search, filter, update, persist.   (Lesson 2, ~45 min)
Run:  python lab2_chroma_basics.py      (then run it AGAIN to see that the data persisted)

Docs: https://docs.trychroma.com
Fill in every TODO. Stuck? Compare with solutions/lab2_chroma_basics.py.
"""

from pathlib import Path

import chromadb

DB_PATH = Path(__file__).resolve().parent / "chroma_db"

FACTS = [
    ("f1", "The Eiffel Tower is in Paris and was completed in 1889.", "travel"),
    ("f2", "Mount Everest is the highest mountain above sea level.", "geography"),
    ("f3", "Python was created by Guido van Rossum and first released in 1991.", "tech"),
    ("f4", "The Dead Sea shore is the lowest land on Earth.", "geography"),
    ("f5", "Git is a distributed version control system.", "tech"),
    ("f6", "The Colosseum in Rome could hold tens of thousands of spectators.", "travel"),
    ("f7", "HTTP status code 404 means the resource was not found.", "tech"),
    ("f8", "The Amazon is the largest rainforest on Earth.", "geography"),
    ("f9", "Machu Picchu is a 15th-century Inca citadel in Peru.", "travel"),
    ("f10", "A Python list is ordered and mutable.", "tech"),
]


def main():
    # TODO 1: create a client that saves to disk:
    #         client = chromadb.PersistentClient(path=str(DB_PATH))
    client = None

    # TODO 2: get_or_create a collection named "lab2_facts" that uses cosine distance:
    #         configuration={"hnsw": {"space": "cosine"}}
    #         Note: get_or_create keeps the space the collection was FIRST created with.
    #         If you ran this once without cosine, delete the chroma_db folder and re-run.
    col = None
    print("Records before adding:", col.count())

    # TODO 3: upsert all FACTS: ids=..., documents=..., metadatas=[{"topic": ...}, ...]
    #         (upsert = insert, or update if the id already exists - safe to re-run)
    print("Records after upsert:", col.count())

    def show(question, **kwargs):
        # TODO 4: res = col.query(query_texts=[question], n_results=3, **kwargs)
        #         then print each document with its distance and topic.
        #         res["documents"][0], res["distances"][0], res["metadatas"][0]
        pass

    show("Which programming language did Guido make?")
    show("Where is the lowest place in the world?")
    # TODO 5: search "famous old buildings" but ONLY in the travel topic:
    #         show("famous old buildings", where={"topic": "travel"})

    # TODO 6: update f7 with new text (col.update), delete f10 (col.delete),
    #         print col.count() and col.get(ids=["f7"])

    # TODO 7 (bonus): create a second collection "lab2_facts_l2" with NO configuration
    #         (default = squared L2). Query both with the same question and compare the
    #         distances. What is the relationship? Is the ranking the same?


if __name__ == "__main__":
    main()

# QUESTIONS
# Q1. Lower distance = more similar or less similar?
# Q2. What happened to "Records before adding" on the second run? Why?
# Q3. Why is a metadata filter (where=...) useful in a real RAG system?

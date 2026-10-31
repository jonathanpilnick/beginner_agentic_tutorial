"""
Lab 2 (SOLUTION) - ChromaDB basics: store, search, filter, update, persist.
Run:  python solutions/lab2_chroma_basics.py      (run it twice: the data persists)
"""

from pathlib import Path

import chromadb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # also works if copied to the main folder
DB_PATH = ROOT / "chroma_db"

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
    # 1. A client that saves to disk (an EphemeralClient() would live only in memory).
    client = chromadb.PersistentClient(path=str(DB_PATH))

    # 2. A collection = a table of (id, text, vector, metadata). We choose cosine distance.
    col = client.get_or_create_collection(
        name="lab2_facts",
        configuration={"hnsw": {"space": "cosine"}},
    )
    print("Records before adding:", col.count())

    # 3. upsert = insert, or update if the id already exists (safe to re-run).
    col.upsert(
        ids=[f[0] for f in FACTS],
        documents=[f[1] for f in FACTS],
        metadatas=[{"topic": f[2]} for f in FACTS],
    )
    print("Records after upsert:", col.count())

    # 4. Similarity search. Chroma embeds the query text with the same model.
    def show(question, **kwargs):
        res = col.query(query_texts=[question], n_results=3, **kwargs)
        print(f"\nQ: {question}  {kwargs if kwargs else ''}")
        for doc, dist, meta in zip(res["documents"][0], res["distances"][0], res["metadatas"][0]):
            print(f"   distance={dist:.3f}  [{meta['topic']}]  {doc}")

    show("Which programming language did Guido make?")
    show("Where is the lowest place in the world?")
    show("famous old buildings", where={"topic": "travel"})       # metadata filter

    # 5. Update one record and delete another.
    col.update(ids=["f7"], documents=["HTTP status code 404 Not Found: the server can't find the page."])
    col.delete(ids=["f10"])
    print("\nAfter delete:", col.count(), "records")
    print("f7 is now:", col.get(ids=["f7"])["documents"][0])

    # 6. Same data, default distance (squared L2). Different numbers, same ranking.
    l2 = client.get_or_create_collection(name="lab2_facts_l2")
    l2.upsert(ids=[f[0] for f in FACTS], documents=[f[1] for f in FACTS])
    q = "Which programming language did Guido make?"
    cos_res = col.query(query_texts=[q], n_results=1)
    l2_res = l2.query(query_texts=[q], n_results=1)
    print(f"\ncosine distance: {cos_res['distances'][0][0]:.3f}   "
          f"squared L2: {l2_res['distances'][0][0]:.3f}   (L2 = 2 x cosine for unit vectors)")


if __name__ == "__main__":
    main()

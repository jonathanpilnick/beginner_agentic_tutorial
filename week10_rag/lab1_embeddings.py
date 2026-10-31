"""
Learn it with your AI tutor: in Claude Code, type
  Be my tutor for Week 10 Lab 1. Read tutor/lab1_embeddings.md completely and follow it.

Lab 1 - Embeddings: turning text into numbers.            (Lesson 1, ~45 min)
Run:  python lab1_embeddings.py

Goal: see what an embedding looks like, compute cosine similarity yourself,
and build a tiny semantic search with no database at all.
Fill in every TODO. Stuck? Compare with solutions/lab1_embeddings.py.
"""

import numpy as np
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Chroma's default embedder = the open-source all-MiniLM-L6-v2 model, run locally (free).
embed = DefaultEmbeddingFunction()

SENTENCES = [
    "The cat sat on the mat.",
    "A kitten is resting on the rug.",
    "Stock markets fell sharply today.",
    "Shares dropped after the earnings report.",
    "How do I reset my password?",
    "I forgot my login credentials.",
    "The football match ended in a draw.",
    "Neither team won the game.",
]


# --- Part A: look at a vector (already done - just run it and read the output) -------
def part_a():
    vectors = np.array(embed(SENTENCES))
    print("Shape (sentences, dimensions):", vectors.shape)
    print("First 8 numbers of sentence 0:", np.round(vectors[0][:8], 3))
    print("Length (L2 norm) of each vector:", np.round(np.linalg.norm(vectors, axis=1), 3))
    return vectors


# --- Part B: cosine similarity by hand -----------------------------------------------
def cosine_similarity(a, b) -> float:
    """cos(a, b) = (a . b) / (|a| * |b|)."""
    # TODO: use np.dot and np.linalg.norm. Return a Python float.
    raise NotImplementedError("TODO: implement cosine_similarity")


def part_b(vectors):
    print("\nPairwise cosine similarity:")
    for i in range(0, len(SENTENCES), 2):
        s = cosine_similarity(vectors[i], vectors[i + 1])
        print(f"  {s:5.2f}  '{SENTENCES[i]}'  vs  '{SENTENCES[i + 1]}'")
    print(f"  {cosine_similarity(vectors[0], vectors[2]):5.2f}  (cat vs stock market)")


# --- Part C: semantic search with no database ------------------------------------------
def semantic_search(query: str, docs: list, doc_vectors, k: int = 3):
    """Return the k most similar docs as a list of (score, doc), best first."""
    # TODO 1: embed the query:  q = np.array(embed([query])[0])
    # TODO 2: compute cosine_similarity(q, d) for every vector d in doc_vectors
    # TODO 3: sort by score, highest first (hint: np.argsort(scores)[::-1][:k])
    raise NotImplementedError("TODO: implement semantic_search")


def keyword_overlap(query: str, doc: str) -> int:
    clean = lambda t: {w.strip(".,?!").lower() for w in t.split()}
    return len(clean(query) & clean(doc))


def part_c(vectors):
    query = "Unable to sign in"           # shares NO words with the best matches
    print(f"\nQuery: {query}")
    for score, doc in semantic_search(query, SENTENCES, vectors):
        print(f"  {score:5.2f}  {doc}   (shared words: {keyword_overlap(query, doc)})")


# --- Part D (bonus): an English-only model on Hebrew -------------------------------------
def part_d():
    hebrew = ["אפשר לעבוד מהבית יומיים בשבוע",      # you can work from home 2 days a week
              "מותר לעבוד מרחוק פעמיים בשבוע",      # remote work is allowed twice a week
              "המניות ירדו היום בבורסה"]             # stocks fell today on the exchange
    v = np.array(embed(hebrew))
    print("\nHebrew test (paraphrase should score higher than the unrelated sentence):")
    print(f"  paraphrase: {cosine_similarity(v[0], v[1]):.2f}")
    print(f"  unrelated : {cosine_similarity(v[0], v[2]):.2f}")


if __name__ == "__main__":
    vecs = part_a()
    part_b(vecs)
    part_c(vecs)
    part_d()

# QUESTIONS - answer in a comment below, then discuss with your neighbour:
# Q1. How many numbers represent one sentence? Does it change for a longer sentence?
# Q2. Every vector has length 1.0. Why does that make cosine similarity equal the dot product?
# Q3. Part C: keyword search would find nothing. Why does semantic search still work?
# Q4. Part D: what went wrong with Hebrew, and what kind of model would fix it?
# Q5. Add 3 sentences of your own and a query. Did the ranking match your intuition?

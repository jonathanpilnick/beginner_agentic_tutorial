"""
Lab 1 (SOLUTION) - Embeddings: turning text into numbers.
Run:  python solutions/lab1_embeddings.py
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


# --- Part A: look at a vector -------------------------------------------------
def part_a():
    vectors = np.array(embed(SENTENCES))
    print("Shape (sentences, dimensions):", vectors.shape)          # (8, 384)
    print("First 8 numbers of sentence 0:", np.round(vectors[0][:8], 3))
    print("Length (L2 norm) of each vector:", np.round(np.linalg.norm(vectors, axis=1), 3))
    return vectors


# --- Part B: cosine similarity by hand ----------------------------------------
def cosine_similarity(a, b) -> float:
    """cos(a, b) = (a . b) / (|a| * |b|).  1 = same direction, 0 = unrelated."""
    a, b = np.asarray(a), np.asarray(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def part_b(vectors):
    print("\nPairwise cosine similarity:")
    for i in range(0, len(SENTENCES), 2):
        s = cosine_similarity(vectors[i], vectors[i + 1])
        print(f"  {s:5.2f}  '{SENTENCES[i]}'  vs  '{SENTENCES[i + 1]}'")
    print(f"  {cosine_similarity(vectors[0], vectors[2]):5.2f}  (cat vs stock market)")


# --- Part C: semantic search with no database ----------------------------------
def semantic_search(query: str, docs: list, doc_vectors, k: int = 3):
    q = np.array(embed([query])[0])
    scores = [cosine_similarity(q, d) for d in doc_vectors]
    best = np.argsort(scores)[::-1][:k]               # highest score first
    return [(float(scores[i]), docs[i]) for i in best]


def keyword_overlap(query: str, doc: str) -> int:
    clean = lambda t: {w.strip(".,?!").lower() for w in t.split()}
    return len(clean(query) & clean(doc))


def part_c(vectors):
    query = "Unable to sign in"           # shares NO words with the best matches
    print(f"\nQuery: {query}")
    for score, doc in semantic_search(query, SENTENCES, vectors):
        print(f"  {score:5.2f}  {doc}   (shared words: {keyword_overlap(query, doc)})")


# --- Part D (bonus): an English-only model on Hebrew ----------------------------
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

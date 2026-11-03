"""
Week 10 · Lab 1 (Day 1): Search your documents by meaning.

You build the "retrieval" half of RAG in 3 short parts:
  Part 1  similarity()             compare two embeddings          (1 line)
  Part 2  chunk_text()             split a document into pieces    (about 6 lines)
  Part 3  build_index(), search()  store chunks in ChromaDB, find the best ones

Run:  python lab1_search.py
      python lab1_search.py "Can I bring my dog to work?"
Each part runs as soon as you finish its TODO.

Your AI tutor: open https://jonathanpilnick.github.io/beginner_agentic_tutorial/week10/lab1
copy the prompt and paste it into Claude Code.
"""

import sys
from pathlib import Path

import chromadb
import numpy as np
from chromadb.errors import NotFoundError
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from pypdf import PdfReader

# Print any character (Hebrew, emoji, arrows) even where the console isn't UTF-8 (Windows).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
DB_PATH = ROOT / "chroma_db"
HANDBOOK = ROOT / "data" / "handbook"

embed_model = DefaultEmbeddingFunction()   # the free all-MiniLM-L6-v2 model, runs on your laptop


def embed(texts):
    """Turn a list of texts into a list of vectors (384 numbers each)."""
    return embed_model(texts)


# ---------- Part 1: similarity ----------------------------------------------
def similarity(a, b):
    """1 = same meaning, 0 = unrelated. Our vectors have length 1,
    so cosine similarity is just the dot product."""
    # TODO 1: return the dot product of a and b as a float.  Hint: np.dot(a, b)
    raise NotImplementedError("TODO 1 in lab1_search.py")


# ---------- Part 2: chunking ------------------------------------------------
def chunk_text(text, size=500, overlap=100):
    """Split text into pieces of `size` characters. Each piece starts
    `size - overlap` characters after the previous one, so neighbours share `overlap`."""
    # TODO 2: start at 0. Repeat while start < len(text):
    #   end = start + size; add text[start:end] to the list;
    #   stop if end reached the end of the text; otherwise start = end - overlap
    raise NotImplementedError("TODO 2 in lab1_search.py")


# ---------- Given: read .txt, .md and .pdf files ----------------------------
def load_documents(folder):
    """Return a list of {"text", "source"}: one per text file, one per PDF page."""
    folder = Path(folder)
    docs = []
    for path in sorted(folder.rglob("*")):
        name = path.relative_to(folder).as_posix()
        if path.suffix.lower() in (".txt", ".md"):
            docs.append({"text": path.read_text(encoding="utf-8", errors="replace"), "source": name})
        elif path.suffix.lower() == ".pdf":
            for page_no, page in enumerate(PdfReader(path).pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    docs.append({"text": text, "source": f"{name} p.{page_no}"})
    return docs


# ---------- Part 3: index and search ----------------------------------------
client = chromadb.PersistentClient(path=str(DB_PATH))


def build_index(folder=HANDBOOK, collection="handbook"):
    """Chunk every document in `folder`, store the chunks in ChromaDB, return how many."""
    try:
        client.delete_collection(collection)   # start fresh every time
    except NotFoundError:
        pass                                   # it didn't exist yet
    col = client.create_collection(collection, configuration={"hnsw": {"space": "cosine"}})
    count = 0
    for doc in load_documents(folder):
        chunks = chunk_text(doc["text"])
        if not chunks:
            continue
        # TODO 3a: store this document's chunks with col.add(ids=..., documents=..., metadatas=...)
        #   ids:       one unique id per chunk, e.g. f"{doc['source']} #{i}" for i in range(len(chunks))
        #   documents: the chunks
        #   metadatas: one {"source": doc["source"]} per chunk (so answers can cite the file)
        count += len(chunks)
    return count


def search(question, k=3, collection="handbook"):
    """The k chunks most similar to the question, best first:
    a list of {"text", "source", "score"} (score = similarity, higher is better)."""
    col = client.get_collection(collection)
    # TODO 3b: res = col.query(query_texts=[question], n_results=k)
    #   res["documents"][0], res["metadatas"][0], res["distances"][0] are lists, best match first.
    #   Return a list of {"text": ..., "source": meta["source"], "score": round(1 - distance, 2)}
    raise NotImplementedError("TODO 3b in lab1_search.py")


# ---------- Run the lab -----------------------------------------------------
QUESTIONS = [
    "Is my puppy allowed in the office?",
    "My laptop is getting old. When do I get a new one?",
    "Who pays for my gym?",
]


def part1():
    print("\n=== Part 1: embeddings and similarity ===")
    pairs = [
        ("Unable to sign in", "I forgot my login credentials"),
        ("The cat sat on the mat", "A kitten is resting on the rug"),
        ("Stock markets fell sharply today", "Share prices dropped"),
        ("The cat sat on the mat", "Stock markets fell sharply today"),
    ]
    v = embed(["Unable to sign in"])[0]
    print(f'"Unable to sign in" -> {len(v)} numbers, starting {[round(float(x), 3) for x in v[:4]]} ...')
    for a, b in pairs:
        va, vb = embed([a, b])
        print(f"  {similarity(va, vb):.2f}   {a}  <->  {b}")


def part2():
    print("\n=== Part 2: chunking ===")
    text = (HANDBOOK / "02_remote_work.md").read_text(encoding="utf-8")
    chunks = chunk_text(text)
    print(f"02_remote_work.md has {len(text)} characters -> {len(chunks)} chunks "
          f"of {[len(c) for c in chunks]} characters")
    print("Chunk 2 starts with:", repr(chunks[1][:60]))


def part3(questions):
    print("\n=== Part 3: index and search ===")
    n = build_index()
    if client.get_collection("handbook").count() == 0:
        raise NotImplementedError("TODO 3a in lab1_search.py")
    print(f"Indexed {n} chunks from {len(load_documents(HANDBOOK))} documents into 'handbook'.")
    for q in questions:
        print(f"\nQ: {q}")
        for r in search(q):
            preview = " ".join(r["text"].split())[:60]
            print(f"  {r['score']:.2f}  {r['source']:28} {preview}...")


if __name__ == "__main__":
    try:
        part1()
        part2()
        part3(sys.argv[1:] or QUESTIONS)
        print("\nAll 3 parts work. Try your own question:  python lab1_search.py \"your question\"")
    except NotImplementedError as todo:
        print(f"\n>>> Next step: {todo}. Finish it, then run the file again.")

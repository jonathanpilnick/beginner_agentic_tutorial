"""
Learn it with your AI tutor: in Claude Code, type
  Be my tutor for Week 10 Lab 3. Read tutor/lab3_ingestion.md completely and follow it.

Lab 3 - Ingestion: load files -> chunk -> embed -> store.    (Lesson 2, ~55 min)
Run:  python lab3_ingest.py                 (indexes data/handbook)
      python lab3_ingest.py path/to/folder  (indexes your own folder)

Labs 4, 5 and the project import build_index() from this file, so finish it!
Stuck? Compare with solutions/lab3_ingest.py, or copy it over this file (it works from either folder).
"""

import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "chroma_db"
DEFAULT_FOLDER = ROOT / "data" / "handbook"
COLLECTION = "handbook"
SUPPORTED = {".txt", ".md", ".pdf"}
MAX_TOKENS = 256          # all-MiniLM-L6-v2 truncates longer inputs


# --- 1. Load ------------------------------------------------------------------
def load_documents(folder: Path) -> list:
    """Return a list of {"text", "source", "page", "archived"} dicts (one per file or PDF page)."""
    docs = []
    for path in sorted(Path(folder).rglob("*")):
        if path.suffix.lower() not in SUPPORTED or not path.is_file():
            continue
        source = path.relative_to(folder).as_posix()
        archived = "archive" in path.relative_to(folder).parts[:-1]
        if path.suffix.lower() == ".pdf":
            # TODO: for each page in PdfReader(path).pages (count pages from 1),
            #       text = page.extract_text(); if it isn't empty, append
            #       {"text": text, "source": source, "page": page_no, "archived": archived}
            pass
        else:
            # TODO: read the file with path.read_text(encoding="utf-8", errors="replace")
            #       and append it with "page": 0
            pass
    return docs


# --- 2. Chunk -----------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list:
    """Split text into ~chunk_size-character pieces that overlap by ~overlap characters."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    text = re.sub(r"\s+", " ", text).strip()        # collapse newlines / repeated spaces
    chunks, start = [], 0
    # TODO: sliding window
    #   while start < len(text):
    #       end = min(start + chunk_size, len(text))
    #       (bonus: move `end` back to the last space so you don't cut a word)
    #       chunks.append(text[start:end])
    #       if end reached the end of the text: break
    #       start = end - overlap
    raise NotImplementedError("TODO: implement chunk_text")


def count_tokens(texts: list) -> list:
    """The real token count of each text. The model only uses the first 256 tokens."""
    tokenizer = ONNXMiniLM_L6_V2().tokenizer   # a private copy: changing it doesn't affect Chroma
    tokenizer.no_truncation()                  # count every token, not just the first 256
    tokenizer.no_padding()                     # don't count [PAD] tokens
    return [len(tokenizer.encode(t).ids) for t in texts]


# --- 3 + 4. Embed and store -------------------------------------------------------
def build_index(folder: Path = DEFAULT_FOLDER, chunk_size: int = 600, overlap: int = 100,
                client=None, collection_name: str = COLLECTION, verbose: bool = True):
    client = client or chromadb.PersistentClient(path=str(DB_PATH))
    try:
        client.delete_collection(collection_name)   # rebuild from scratch every time
    except Exception:                                # noqa: BLE001 - it didn't exist yet
        pass
    col = client.create_collection(collection_name, configuration={"hnsw": {"space": "cosine"}})

    ids, texts, metas = [], [], []
    for doc in load_documents(folder):
        for i, chunk in enumerate(chunk_text(doc["text"], chunk_size, overlap)):
            # TODO: append a unique id like f"{doc['source']}::p{doc['page']}::c{i}",
            #       the chunk text, and metadata {"source", "page", "chunk", "archived"}
            pass
    if not texts:
        raise SystemExit(f"No chunks created from {folder} - check your TODOs above")

    # TODO: add to the collection in batches of 100:
    #       col.add(ids=ids[b:b+100], documents=texts[b:b+100], metadatas=metas[b:b+100])

    if verbose:
        tokens = count_tokens(texts)
        too_long = sum(t > MAX_TOKENS for t in tokens)
        print(f"Indexed {len(texts)} chunks from {len({m['source'] for m in metas})} files "
              f"into '{collection_name}'.")
        print(f"Tokens per chunk: min {min(tokens)}, max {max(tokens)}, "
              f"avg {sum(tokens) / len(tokens):.0f}.  Truncated (> {MAX_TOKENS}): {too_long}")
    return col


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FOLDER
    collection = build_index(folder)
    sample = collection.get(limit=2)
    for cid, text in zip(sample["ids"], sample["documents"]):
        print(f"\n{cid}\n  {text[:160]}...")

# QUESTIONS
# Q1. How many chunks did the handbook produce? How many came from the PDF?
# Q2. Run with chunk_size=2000. How many chunks are now longer than 256 tokens? What does
#     the embedding model do with the extra text?
# Q3. Why do we store "source" and "page" in the metadata?
# Q4. Why overlap? What could go wrong with overlap=0?

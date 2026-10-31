"""
Lab 3 (SOLUTION) - Ingestion: load files -> chunk -> embed -> store.
Run:  python solutions/lab3_ingest.py                 (indexes data/handbook)
      python solutions/lab3_ingest.py path/to/folder  (indexes your own folder)
"""

import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # also works if copied to the main folder
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
            for page_no, page in enumerate(PdfReader(path).pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    docs.append({"text": text, "source": source, "page": page_no, "archived": archived})
        else:
            text = path.read_text(encoding="utf-8", errors="replace")   # always say utf-8 on Windows
            docs.append({"text": text, "source": source, "page": 0, "archived": archived})
    return docs


# --- 2. Chunk -----------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list:
    """Split text into ~chunk_size-character pieces that overlap by ~overlap characters.
    Cuts at a space so words are not broken in half."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    text = re.sub(r"\s+", " ", text).strip()        # collapse newlines / repeated spaces
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):                          # try not to cut a word in half
            space = text.rfind(" ", start, end)
            if space > start + chunk_size // 2:
                end = space
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)        # step back to create the overlap
        space = text.find(" ", start, end)           # ...and start on a word boundary
        if space != -1:
            start = space + 1
    return [c for c in chunks if c]


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
            ids.append(f"{doc['source']}::p{doc['page']}::c{i}")
            texts.append(chunk)
            metas.append({"source": doc["source"], "page": doc["page"],
                          "chunk": i, "archived": doc["archived"]})
    if not texts:
        raise SystemExit(f"No .txt/.md/.pdf files found in {folder}")

    for b in range(0, len(texts), 100):              # add in batches
        col.add(ids=ids[b:b + 100], documents=texts[b:b + 100], metadatas=metas[b:b + 100])

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

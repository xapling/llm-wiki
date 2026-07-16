"""RAG-Seite: Korpus chunken und in Chroma indexieren.

Bewusst klassisch gehalten: Absatz-basiertes Chunking (~900 Zeichen),
lokale Embeddings (mehrsprachiges MiniLM — der Korpus ist deutsch).
Genau so sähe ein typischer erster RAG-Aufbau aus.
"""

# app.common zuerst: setzt Umgebungsvariablen, bevor chromadb lädt
from app.common import CHROMA_DIR, CORPUS_DIR

import chromadb
from chromadb.utils import embedding_functions

COLLECTION = "corpus"
CHUNK_CHARS = 900
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def _embedding_fn():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )


def chunk_document(text: str) -> list[str]:
    """Absätze greedy zu Chunks von ~CHUNK_CHARS zusammenfassen."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        if current and len(current) + len(para) > CHUNK_CHARS:
            chunks.append(current.strip())
            current = ""
        current += para + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks


def get_collection():
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return db.get_or_create_collection(COLLECTION, embedding_function=_embedding_fn())


def _doc_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_index() -> int:
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        db.delete_collection(COLLECTION)
    except Exception:
        pass
    col = db.get_or_create_collection(COLLECTION, embedding_function=_embedding_fn())

    ids, docs, metas = [], [], []
    for doc_path in sorted(CORPUS_DIR.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        title = _doc_title(text, doc_path.stem)
        for i, chunk in enumerate(chunk_document(text)):
            ids.append(f"{doc_path.stem}#{i}")
            # Titel-Präfix: auch Chunks aus der Dokumentmitte behalten ihren
            # Kontext — Standard-Kniff für besseres Retrieval
            docs.append(f"[Dokument: {title}]\n{chunk}")
            metas.append({"source": doc_path.name, "chunk": i})

    col.add(ids=ids, documents=docs, metadatas=metas)
    return len(ids)


if __name__ == "__main__":
    n_docs = len(list(CORPUS_DIR.glob("*.md")))
    n_chunks = build_index()
    print(f"Index gebaut: {n_docs} Dokumente → {n_chunks} Chunks.")

"""Klassisches RAG: Frage embedden, Top-k-Chunks holen, Antwort generieren."""

import time

from app.common import MODEL, BackendResult, client
from app.indexer import get_collection

TOP_K = 5

SYSTEM = """Du bist ein Assistent für das interne Firmenwissen der SolarFlow GmbH.

Beantworte die Frage ausschließlich auf Basis der bereitgestellten Auszüge aus
internen Dokumenten. Nenne am Ende die Quelldokumente, die du verwendet hast.
Wenn die Auszüge widersprüchlich oder unvollständig sind, gib wieder, was in
ihnen steht — du hast keinen weiteren Kontext. Antworte auf Deutsch."""


def answer(question: str) -> BackendResult:
    start = time.time()

    col = get_collection()
    res = col.query(query_texts=[question], n_results=TOP_K)
    docs = res["documents"][0]
    metas = res["metadatas"][0]

    context_items = [
        {"label": f"Chunk aus {meta['source']} (#{meta['chunk']})", "content": doc}
        for doc, meta in zip(docs, metas)
    ]

    excerpts = "\n\n---\n\n".join(
        f"[Auszug {i + 1} — Quelle: {meta['source']}]\n{doc}"
        for i, (doc, meta) in enumerate(zip(docs, metas))
    )

    response = client().chat.completions.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Auszüge:\n\n{excerpts}\n\nFrage: {question}",
            },
        ],
    )

    usage = response.usage
    return BackendResult(
        answer=response.choices[0].message.content or "",
        context_items=context_items,
        input_tokens=usage.prompt_tokens if usage else 0,
        output_tokens=usage.completion_tokens if usage else 0,
        seconds=time.time() - start,
    )

"""Antworten der Drehbuch-Fragen aufzeichnen — Grundlage für den Replay-Modus.

Am besten einmal VOR dem Ingest (Fragen 1-3) und einmal NACH `make ingest`
laufen lassen (Fragen 4-5 beziehen sich auf den Zustand nach dem Ingest);
der Cache wird pro Frage überschrieben, Wiederholen ist unkritisch.
"""

from app import rag_backend, wiki_backend
from app.common import SCRIPTED_QUESTIONS, save_cached


def main() -> None:
    for i, question in enumerate(SCRIPTED_QUESTIONS, 1):
        print(f"[{i}/{len(SCRIPTED_QUESTIONS)}] {question}")
        for name, backend in (("rag", rag_backend), ("wiki", wiki_backend)):
            result = backend.answer(question)
            save_cached(name, question, result)
            print(f"    {name}: {result.seconds:.1f}s, "
                  f"{result.input_tokens}→{result.output_tokens} Tokens")
    print("\nCache geschrieben nach demo/cache/ — Replay-Modus ist einsatzbereit.")


if __name__ == "__main__":
    main()

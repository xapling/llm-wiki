"""Live-Ingest-Demo: ein neues Dokument in beide Welten einspeisen.

RAG-Seite:  Dokument in corpus/ kopieren, Index neu bauen. Fertig — und genau
            das ist der Punkt: Es wurde nichts verstanden, nichts verknüpft.
Wiki-Seite: Ein Agent liest das Dokument, aktualisiert betroffene Wiki-Seiten,
            legt neue an, setzt Querverweise und schreibt einen Log-Eintrag —
            live im Terminal mitzuverfolgen.
"""

import json
import shutil
import sys
import time
from datetime import date
from pathlib import Path

from app.common import CORPUS_DIR, MODEL, WIKI_DIR, client
from app.indexer import build_index
from app.wiki_backend import _safe_wiki_path, read_page

MAX_TURNS = 25

SYSTEM = f"""Du pflegst das interne Wissens-Wiki der SolarFlow GmbH (Open
Knowledge Format: Markdown mit YAML-Frontmatter, index.md pro Bereich,
Querverweise als Links auf Wiki-Pfade wie /systeme/api-gateway.md).

Deine Aufgabe: Ein neues Quelldokument in das Wiki INTEGRIEREN (Ingest).

Vorgehen:
1. Lies zuerst index.md und die Bereichs-Indizes, die relevant sein könnten.
2. Lies die bestehenden Seiten, die das Dokument berührt.
3. Aktualisiere betroffene Seiten: neue Fakten einarbeiten, Widersprüche
   EXPLIZIT auflösen (was gilt jetzt, was ist veraltet — mit Datum), offene
   Fragen schließen, wenn das Dokument sie beantwortet.
4. Lege neue Seiten an, wo ein Konzept noch keine Seite hat (z. B. ein Kunde,
   ein Vorfall). Frontmatter: type, title, description, tags, timestamp,
   sources (Pfad des Quelldokuments).
5. Setze Querverweise in BEIDE Richtungen und aktualisiere die betroffenen
   index.md-Seiten (Tabellen/Listen).
6. Schreibe zum Schluss einen neuen Eintrag OBEN in log.md (Datum {date.today().isoformat()},
   Operation "Ingest", Quelle, berührte Seiten) — bestehende Einträge bleiben.

Regeln: Quelldokumente sind unveränderlich — du schreibst nur ins Wiki.
Schreibe auf Deutsch, im Stil der bestehenden Seiten. Wenn du eine Seite
änderst, schreibe sie IMMER vollständig (write_page überschreibt).
Wenn du fertig bist, fasse in 3-5 Sätzen zusammen, was du integriert hast."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": "Liest eine Wiki-Seite. Pfad relativ zur Wiki-Wurzel.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_page",
            "description": (
                "Schreibt eine Wiki-Seite (überschreibt vollständig oder legt "
                "neu an). Pfad relativ zur Wiki-Wurzel."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
]


def write_page(path: str, content: str) -> str:
    target, rel = _safe_wiki_path(path)
    existed = target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"{'Aktualisiert' if existed else 'Neu angelegt'}: {rel}"


def ingest_rag(doc: Path) -> dict:
    """RAG-Seite: Dokument ablegen, Index neu bauen. Mehr passiert nicht."""
    start = time.time()
    shutil.copy(doc, CORPUS_DIR / doc.name)
    n_chunks = build_index()
    return {"seconds": time.time() - start, "chunks": n_chunks}


def ingest_wiki(doc: Path, on_step=None) -> dict:
    """Wiki-Seite: Agent integriert das Dokument.

    on_step(kind, text) wird für jeden Schritt gerufen (kind: 'read'|'write'),
    damit UI und Terminal live mitzeigen können.
    """
    start = time.time()
    source_text = doc.read_text(encoding="utf-8")

    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                f"Neues Quelldokument (liegt jetzt unter corpus/{doc.name}):\n\n"
                f"{source_text}\n\nIntegriere es in das Wiki."
            ),
        },
    ]

    pages_written: list[str] = []
    msg = None
    for _ in range(MAX_TURNS):
        response = client().chat.completions.create(
            model=MODEL,
            max_tokens=8192,
            tools=TOOLS,
            messages=messages,
        )
        msg = response.choices[0].message
        if not msg.tool_calls:
            break

        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )
        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
                if tc.function.name == "read_page":
                    rel = args["path"].lstrip("/")
                    if on_step:
                        on_step("read", rel)
                    result = read_page(args["path"])
                elif tc.function.name == "write_page":
                    rel = args["path"].lstrip("/")
                    if on_step:
                        on_step("write", rel)
                    result = write_page(args["path"], args["content"])
                    pages_written.append(rel)
                else:
                    result = f"FEHLER: unbekanntes Werkzeug {tc.function.name}"
            except Exception as exc:
                result = f"FEHLER: {exc}"
            messages.append(
                {"role": "tool", "tool_call_id": tc.id, "content": result}
            )

    return {
        "seconds": time.time() - start,
        "pages": pages_written,
        "summary": (msg.content or "") if msg else "",
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Aufruf: python -m app.ingest <pfad-zum-dokument.md>")
        sys.exit(1)
    doc = Path(sys.argv[1])
    if not doc.exists():
        print(f"Dokument nicht gefunden: {doc}")
        sys.exit(1)
    if not WIKI_DIR.exists():
        print("wiki/ fehlt — bitte zuerst `make reset` ausführen.")
        sys.exit(1)

    print(f"\nIngest von: {doc.name}\n")

    print("━" * 72)
    print("RAG-Seite")
    print("━" * 72)
    rag = ingest_rag(doc)
    print(f"  Dokument nach corpus/ kopiert, Index neu gebaut ({rag['chunks']} Chunks).")
    print(f"  Fertig in {rag['seconds']:.1f}s. Verknüpft wurde: nichts.\n")

    print("━" * 72)
    print("Wiki-Seite — der Agent integriert das Dokument")
    print("━" * 72)
    icons = {"read": "📖 liest   ", "write": "✍️  schreibt"}
    wiki = ingest_wiki(doc, on_step=lambda k, t: print(f"  {icons[k]} {t}"))
    print("\n  Zusammenfassung des Agenten:\n")
    for line in wiki["summary"].strip().splitlines():
        print(f"    {line}")
    print(f"\n  Fertig in {wiki['seconds']:.1f}s — "
          f"{len(wiki['pages'])} Seiten geschrieben: {', '.join(wiki['pages'])}")


if __name__ == "__main__":
    main()

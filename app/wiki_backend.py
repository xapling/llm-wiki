"""LLM-Wiki: Agent navigiert das OKF-Bundle über index.md und liest Konzeptseiten.

Bewusst als sichtbare Werkzeugschleife implementiert (kein Framework), damit
im Code nachvollziehbar bleibt, was der Agent tut: Seite lesen → entscheiden →
nächste Seite lesen → antworten. Erkenntnisse kann er unter analysen/ ablegen.
"""

import json
import re
import time
from datetime import date

from app.common import MODEL, WIKI_DIR, BackendResult, client

MAX_TURNS = 12

SYSTEM = """Du beantwortest Fragen über die SolarFlow GmbH auf Basis ihres
internen Wissens-Wikis (Open Knowledge Format: Markdown-Seiten mit
YAML-Frontmatter, verlinkt über index.md-Seiten).

Vorgehen:
1. Die Einstiegsseite (index.md) bekommst du mitgeliefert.
2. Navigiere von dort gezielt: Lies mit read_page nur die Seiten, die für die
   Frage relevant sind. Folge Links im Text (Pfade wie /systeme/api-gateway.md).
3. Antworte auf Deutsch, präzise und mit Verweis auf die Wiki-Seiten und die
   dort genannten Quelldokumente.

save_analysis nutzt du NUR, wenn die Frage AUSDRÜCKLICH nach Mustern, einer
Analyse oder einer Bewertung fragt (z. B. "Welche Muster erkennst du …?").
Fakten- und Aufzählungsfragen ("Was ist …", "Welche … gab es …") beantwortest
du nur — ohne zu speichern. Wenn du gespeichert hast, erwähne das am Ende
deiner Antwort in einem Satz (mit Seitenpfad): Diese Erkenntnis bleibt dem
Wiki dauerhaft erhalten.

Wichtig: Gib deine vollständige Antwort IMMER als Text aus — auch dann, wenn
du im selben Zug ein Werkzeug aufrufst."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": (
                "Liest eine Seite aus dem Wiki. Pfad relativ zur Wiki-Wurzel, "
                "z. B. 'systeme/api-gateway.md' oder '/kunden/index.md'."
            ),
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
            "name": "save_analysis",
            "description": (
                "Speichert eine Analyse/Erkenntnis als neue Wiki-Seite unter "
                "analysen/. Nur für übertragbare Erkenntnisse nutzen, nicht "
                "für einfache Faktenantworten."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": "Dateiname ohne .md, kebab-case",
                    },
                    "title": {"type": "string"},
                    "content": {
                        "type": "string",
                        "description": "Markdown-Inhalt der Analyse",
                    },
                },
                "required": ["slug", "title", "content"],
            },
        },
    },
]


def _safe_wiki_path(path: str):
    rel = path.strip().lstrip("/")
    target = (WIKI_DIR / rel).resolve()
    if not target.is_relative_to(WIKI_DIR.resolve()):
        raise ValueError(f"Pfad außerhalb des Wikis: {path}")
    return target, rel


def read_page(path: str) -> str:
    target, _ = _safe_wiki_path(path)
    if not target.exists():
        return f"FEHLER: Seite '{path}' existiert nicht."
    return target.read_text(encoding="utf-8")


def save_analysis(slug: str, title: str, content: str) -> str:
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-") or "analyse"
    rel = f"analysen/{slug}.md"
    target, _ = _safe_wiki_path(rel)
    today = date.today().isoformat()

    page = (
        "---\n"
        f"type: Analyse\n"
        f"title: {title}\n"
        f"description: Aus einer Anfrage gespeicherte Erkenntnis ({today}).\n"
        f"tags: [analysen]\n"
        f"timestamp: {today}T00:00:00Z\n"
        "---\n\n"
        f"# {title}\n\n{content.strip()}\n"
    )
    target.write_text(page, encoding="utf-8")

    # In den Analysen-Index eintragen
    index_path = WIKI_DIR / "analysen" / "index.md"
    index = index_path.read_text(encoding="utf-8")
    index = index.replace("*Noch keine gespeicherten Analysen.*", "").rstrip()
    index += f"\n\n- [{title}](/analysen/{slug}.md) — gespeichert am {today}\n"
    index_path.write_text(index, encoding="utf-8")

    # Log-Eintrag oben anfügen (nach dem Einleitungsblock)
    log_path = WIKI_DIR / "log.md"
    log = log_path.read_text(encoding="utf-8")
    entry = (
        f"## {today} · Query → Analyse gespeichert\n\n"
        f"Neue Seite: [{slug}](/analysen/{slug}.md) — aus einer Anfrage "
        f"entstandene Erkenntnis.\n\n"
    )
    marker = "Neueste Einträge oben."
    pos = log.find(marker)
    if pos != -1:
        insert_at = log.index("\n\n", pos) + 2
        log = log[:insert_at] + entry + log[insert_at:]
    else:
        log += "\n" + entry
    log_path.write_text(log, encoding="utf-8")

    return f"Gespeichert als {rel} (Index und Log aktualisiert)."


def _execute_tool_call(tool_call, pages_read: list) -> str:
    args = json.loads(tool_call.function.arguments or "{}")
    if tool_call.function.name == "read_page":
        result = read_page(args["path"])
        pages_read.append({"label": args["path"].lstrip("/"), "content": result})
        return result
    if tool_call.function.name == "save_analysis":
        result = save_analysis(**args)
        pages_read.append(
            {
                "label": f"✍️ gespeichert: analysen/{args['slug']}.md",
                "content": args["content"],
            }
        )
        return result
    return f"FEHLER: unbekanntes Werkzeug {tool_call.function.name}"


def answer(question: str) -> BackendResult:
    start = time.time()
    pages_read: list[dict] = []
    total_in = total_out = 0

    entry_page = read_page("index.md")
    pages_read.append({"label": "index.md (Einstieg)", "content": entry_page})

    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                f"Einstiegsseite des Wikis (index.md):\n\n{entry_page}\n\n"
                f"Frage: {question}"
            ),
        },
    ]

    # Antworttexte über alle Züge sammeln: Der Agent antwortet oft im selben Zug,
    # in dem er noch ein Werkzeug aufruft — nur der letzte Zug wäre zu wenig.
    answer_parts: list[str] = []
    msg = None
    for _ in range(MAX_TURNS):
        response = client().chat.completions.create(
            model=MODEL,
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )
        if response.usage:
            total_in += response.usage.prompt_tokens
            total_out += response.usage.completion_tokens

        msg = response.choices[0].message
        if msg.content and msg.content.strip():
            answer_parts.append(msg.content.strip())
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
                result = _execute_tool_call(tc, pages_read)
            except Exception as exc:  # Fehler zurückspielen statt abbrechen
                result = f"FEHLER: {exc}"
            messages.append(
                {"role": "tool", "tool_call_id": tc.id, "content": result}
            )

    return BackendResult(
        answer="\n\n".join(answer_parts),
        context_items=pages_read,
        input_tokens=total_in,
        output_tokens=total_out,
        seconds=time.time() - start,
    )

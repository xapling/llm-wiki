"""Gemeinsame Basis: Pfade, Modell, Ergebnis-Struktur, Antwort-Cache (Replay).

Alle LLM-Aufrufe laufen ausschließlich über OpenRouter (OpenAI-kompatible API)
mit genau einem Modell (MODEL). Schlüssel: OPENROUTER_API_KEY aus .env.local
oder .env.
"""

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent

# Konsolen-Lärm der Bibliotheken abstellen (muss vor deren Import passieren)
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")   # HuggingFace-Fork-Warnung
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")     # Chroma-Telemetrie

CORPUS_DIR = ROOT / "corpus"
WIKI_DIR = ROOT / "wiki"
CHROMA_DIR = ROOT / ".chroma"
CACHE_DIR = ROOT / "demo" / "cache"

MODEL = "anthropic/claude-opus-4.8"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Die Drehbuch-Fragen (siehe demo/drehbuch.md)
SCRIPTED_QUESTIONS = [
    "Welchen Message-Broker setzen wir ein und wofür?",
    "Warum hat Helios Energie gekündigt? Erzähl die ganze Geschichte.",
    "Wie viele Requests pro Minute erlaubt unsere öffentliche API?",
    "Welche Vorfälle gab es 2026 und was waren jeweils die Ursachen?",
    "Welche wiederkehrenden Muster erkennst du in unseren Vorfällen von 2026?",
]


def _load_dotenv() -> None:
    """Liest .env und .env.local (KEY=WERT pro Zeile), ohne gesetzte Variablen zu überschreiben."""
    for name in (".env", ".env.local"):
        env_file = ROOT / name
        if not env_file.exists():
            continue
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


_load_dotenv()

_client = None


def client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY fehlt — bitte in .env.local eintragen."
            )
        _client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    return _client


COMPARE_SYSTEM = """Du vergleichst zwei Antworten auf dieselbe Frage über
internes Firmenwissen. Antwort A stammt von einem RAG-System (rohe
Text-Schnipsel), Antwort B von einem LLM-Wiki (kuratierte Seiten).

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt (kein Text davor/danach):

{
  "summary": "2-4 kurze Stichpunkte (mit '- ', durch \\n getrennt) zum INHALTLICHEN Unterschied: Welche Fakten/Zusammenhänge fehlen wem? Wer nennt Veraltetes oder lässt Widersprüche ungeklärt? Wer bleibt unsicher, wo der andere konkret wird?",
  "rag_highlights": ["bis zu 3 wörtliche Zitate aus Antwort A (je 3-12 Wörter): Stellen, die lückenhaft, veraltet, widersprüchlich oder unsicher sind"],
  "wiki_highlights": ["bis zu 3 wörtliche Zitate aus Antwort B (je 3-12 Wörter): die entscheidenden Inhalte, die Antwort A fehlen"]
}

Regeln:
- Zitate müssen ZEICHENGENAU so in der jeweiligen Antwort vorkommen
  (Copy-Paste, inklusive Formatierung wie **), keine Auslassungen, keine
  eckigen Klammern im Zitat.
- Sei streng fair und nüchtern — kein Marketing. Sind beide Antworten
  inhaltlich gleichwertig: summary = "- Beide Antworten sind inhaltlich
  gleichwertig. ✅" und beide Listen leer.
- Bewerte nur Inhalt, nicht Stil. Deutsch."""


def compare_answers(question: str, rag_answer: str, wiki_answer: str) -> dict:
    """Inhaltlicher Vergleich: Stichpunkte + wörtliche Zitate zum Hervorheben.

    Rückgabe: {"summary": str, "rag_highlights": [str], "wiki_highlights": [str]}
    """
    response = client().chat.completions.create(
        model=MODEL,
        max_tokens=800,
        messages=[
            {"role": "system", "content": COMPARE_SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Frage: {question}\n\n"
                    f"--- Antwort A (RAG) ---\n{rag_answer}\n\n"
                    f"--- Antwort B (LLM-Wiki) ---\n{wiki_answer}"
                ),
            },
        ],
    )
    text = (response.choices[0].message.content or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    try:
        data = json.loads(text[text.find("{"): text.rfind("}") + 1])
    except (ValueError, TypeError):
        return {"summary": text, "rag_highlights": [], "wiki_highlights": []}
    return {
        "summary": str(data.get("summary", "")),
        "rag_highlights": [str(q) for q in data.get("rag_highlights", [])],
        "wiki_highlights": [str(q) for q in data.get("wiki_highlights", [])],
    }


def apply_highlights(text: str, quotes: list, color: str) -> str:
    """Hinterlegt wörtliche Zitate farbig (Streamlit-Markdown-Syntax)."""
    for quote in sorted(set(quotes), key=len, reverse=True):
        quote = quote.strip()
        if len(quote) < 3 or "[" in quote or "]" in quote:
            continue
        if quote in text and f"-background[{quote}]" not in text:
            text = text.replace(quote, f":{color}-background[{quote}]", 1)
    return text


@dataclass
class BackendResult:
    """Antwort eines Backends inkl. allem, was die UI sichtbar macht."""

    answer: str
    # Was das System gesehen hat: [{"label": ..., "content": ...}, ...]
    context_items: list = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "BackendResult":
        return BackendResult(**d)


def _cache_path(backend: str, question: str) -> Path:
    key = hashlib.sha256(f"{backend}::{question.strip()}".encode()).hexdigest()[:16]
    return CACHE_DIR / f"{backend}-{key}.json"


def save_cached(backend: str, question: str, result: BackendResult) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"question": question, "result": result.to_dict()}
    _cache_path(backend, question).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_cached(backend: str, question: str) -> BackendResult | None:
    path = _cache_path(backend, question)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return BackendResult.from_dict(payload["result"])

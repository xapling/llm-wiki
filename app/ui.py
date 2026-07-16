"""Streamlit-UI: RAG und LLM-Wiki side-by-side — Fragen stellen und Daten einspeisen."""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json  # noqa: E402

from app import rag_backend, wiki_backend  # noqa: E402
from app.common import (  # noqa: E402
    CORPUS_DIR,
    ROOT,
    SCRIPTED_QUESTIONS,
    WIKI_DIR,
    BackendResult,
    apply_highlights,
    compare_answers,
    load_cached,
    save_cached,
)
from app.ingest import ingest_rag, ingest_wiki  # noqa: E402

EINGANG_DIR = ROOT / "demo" / "eingang"

st.set_page_config(page_title="RAG vs. LLM-Wiki", layout="wide")

st.title("RAG vs. LLM-Wiki")
st.caption(
    "Gleiche Frage, gleiches Wissen, zwei Architekturen — links klassisches "
    "RAG (Chunks + Embeddings), rechts das LLM-Wiki (kuratiertes OKF-Bundle)."
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Demo-Steuerung")
    replay = st.toggle(
        "Replay-Modus (ohne API)",
        value=False,
        help="Spielt mit `make record` aufgezeichnete Antworten ab — Fallback "
        "bei WLAN-/API-Problemen.",
    )
    st.subheader("Drehbuch-Fragen")
    for i, q in enumerate(SCRIPTED_QUESTIONS, 1):
        if st.button(f"Akt {i}", help=q, use_container_width=True):
            st.session_state["question"] = q

    if not WIKI_DIR.exists():
        st.error("`wiki/` fehlt — bitte zuerst `make reset` ausführen.")

tab_fragen, tab_ingest, tab_info = st.tabs(
    ["💬 Fragen stellen", "📥 Neues Dokument einspeisen", "ℹ️ Wie funktioniert das?"]
)

# ═════════════════════════════════════════════════════════════════ Fragen ═══
with tab_fragen:
    question = st.text_input(
        "Frage an das Firmenwissen",
        value=st.session_state.get("question", ""),
        placeholder="z. B.: Warum hat Helios Energie gekündigt?",
    )

    ask = st.button("Beide Backends fragen", type="primary", disabled=not question)

    def run_backend(name: str, backend) -> BackendResult:
        if replay:
            cached = load_cached(name, question)
            if cached is None:
                return BackendResult(
                    answer="_Keine aufgezeichnete Antwort für diese Frage — "
                    "`make record` ausführen oder Replay-Modus deaktivieren._"
                )
            return cached
        try:
            result = backend.answer(question)
        except Exception as exc:
            hint = ""
            text = str(exc).lower()
            if any(m in text for m in ("authentication", "401", "openrouter_api_key")):
                hint = (
                    "\n\n💡 `OPENROUTER_API_KEY` in `.env.local` eintragen und die "
                    "App neu starten (oder Replay-Modus aktivieren, falls "
                    "Antworten aufgezeichnet sind)."
                )
            return BackendResult(answer=f"⚠️ **Fehler:** {exc}{hint}")
        save_cached(name, question, result)  # jede Live-Antwort ist künftiger Fallback
        return result

    def render(
        col,
        title: str,
        subtitle: str,
        result: BackendResult,
        kind: str = "rag",
        highlights: list | None = None,
    ) -> None:
        with col:
            st.subheader(title)
            st.caption(subtitle)
            answer = result.answer
            if highlights:
                color = "orange" if kind == "rag" else "green"
                answer = apply_highlights(answer, highlights, color)
            st.markdown(answer)

            # Wiki-Vorteile sichtbar machen: gespeicherte Erkenntnisse + Lesepfad
            saved = [i for i in result.context_items if i["label"].startswith("✍️")]
            for item in saved:
                page = item["label"].replace("✍️ gespeichert: ", "")
                st.success(
                    f"💾 **Erkenntnis dauerhaft gespeichert:** `{page}` — bleibt im "
                    f"Wiki und muss nie wieder neu hergeleitet werden."
                )
            if kind == "wiki" and result.context_items:
                path = " → ".join(
                    i["label"].split(" (")[0]
                    for i in result.context_items
                    if not i["label"].startswith("✍️")
                )
                st.caption(f"🧭 Gelesener Pfad: {path}")

            if result.seconds:
                st.caption(
                    f"⏱ {result.seconds:.1f} s · Tokens: {result.input_tokens:,} rein / "
                    f"{result.output_tokens:,} raus".replace(",", ".")
                )
            with st.expander(f"Was hat das System gesehen? ({len(result.context_items)})"):
                for item in result.context_items:
                    st.markdown(f"**{item['label']}**")
                    st.code(item["content"][:1200], language="markdown")

    def run_comparison(rag_result: BackendResult, wiki_result: BackendResult) -> dict | None:
        """Inhaltlichen Vergleich holen (live) bzw. aus dem Cache lesen (Replay)."""
        if replay:
            cached = load_cached("diff", question)
            if cached is None:
                return None
            try:
                return json.loads(cached.answer)
            except ValueError:  # ältere Cache-Einträge: nur Stichpunkte
                return {"summary": cached.answer, "rag_highlights": [], "wiki_highlights": []}
        # Nur vergleichen, wenn beide Seiten echte Antworten geliefert haben
        if not rag_result.context_items or not wiki_result.context_items:
            return None
        try:
            diff = compare_answers(question, rag_result.answer, wiki_result.answer)
        except Exception:
            return None
        save_cached("diff", question, BackendResult(answer=json.dumps(diff, ensure_ascii=False)))
        return diff

    def render_diff(
        rag_result: BackendResult,
        wiki_result: BackendResult,
        content_diff: dict | None,
    ) -> None:
        """Die Unterschiede dieses konkreten Antwortpaars auf den Punkt bringen."""
        summary = (content_diff or {}).get("summary", "").strip()
        if not summary and not rag_result.context_items and not wiki_result.context_items:
            return
        wiki_pages = [
            i["label"].split(" (")[0]
            for i in wiki_result.context_items
            if not i["label"].startswith("✍️")
        ]
        saved = [i for i in wiki_result.context_items if i["label"].startswith("✍️")]
        rag_sources = {
            i["label"].split(" (")[0].replace("Chunk aus ", "")
            for i in rag_result.context_items
        }

        lines = []
        if summary:
            lines.append("#### 💡 Der inhaltliche Unterschied")
            lines.append(summary)
            lines.append("")
            lines.append("**So kam es dazu:**")
        else:
            lines.append("#### 💡 Was lief hier anders?")
        if rag_result.context_items:
            lines.append(
                f"- 🧩 **RAG** hat {len(rag_result.context_items)} Text-Schnipsel "
                f"aus {len(rag_sources)} Dokumenten per Ähnlichkeit gezogen — "
                f"Fragmente, ohne zu wissen, was zusammengehört oder was aktuell gilt."
            )
        if wiki_pages:
            lines.append(
                f"- 📚 **Das Wiki** ist gezielt dem Wissensnetz gefolgt "
                f"({' → '.join(wiki_pages)}) — kuratierte Seiten, auf denen "
                f"Widersprüche schon geklärt und Quellen verlinkt sind."
            )
        if saved:
            page = saved[0]["label"].replace("✍️ gespeichert: ", "")
            lines.append(
                f"- 💾 **Das kann nur das Wiki:** Die Erkenntnis wurde als neue "
                f"Seite `{page}` gespeichert — bei der nächsten Frage ist sie "
                f"sofort da. RAG hätte sie weggeworfen."
            )
        st.info("\n".join(lines))

    if ask and question:
        with st.spinner("Beide Backends arbeiten …"):
            with ThreadPoolExecutor(max_workers=2) as pool:
                rag_future = pool.submit(run_backend, "rag", rag_backend)
                wiki_future = pool.submit(run_backend, "wiki", wiki_backend)
                rag_result = rag_future.result()
                wiki_result = wiki_future.result()

        with st.spinner("Vergleiche die Antworten inhaltlich …"):
            content_diff = run_comparison(rag_result, wiki_result)

        if content_diff and (
            content_diff.get("rag_highlights") or content_diff.get("wiki_highlights")
        ):
            st.caption(
                "Markiert: 🟧 lückenhaft, veraltet oder unsicher · "
                "🟩 entscheidender Inhalt, der der anderen Antwort fehlt"
            )

        left, right = st.columns(2)
        render(
            left,
            "🧩 RAG",
            "Top-5-Chunks per Embedding-Ähnlichkeit → Antwort aus Fragmenten",
            rag_result,
            kind="rag",
            highlights=(content_diff or {}).get("rag_highlights"),
        )
        render(
            right,
            "📚 LLM-Wiki",
            "Navigiert index.md → liest kuratierte Konzeptseiten → Antwort mit Kontext",
            wiki_result,
            kind="wiki",
            highlights=(content_diff or {}).get("wiki_highlights"),
        )
        render_diff(rag_result, wiki_result, content_diff)

# ═════════════════════════════════════════════════════════════════ Ingest ═══
with tab_ingest:
    st.markdown(
        "**Der Use Case:** Ein neues Dokument kommt an — etwa ein frischer "
        "Störungsbericht. Was machen die beiden Systeme daraus?"
    )

    eingang_docs = {p.name: p for p in sorted(EINGANG_DIR.glob("*.md"))}
    col_sel, col_up = st.columns(2)
    with col_sel:
        selected_name = st.selectbox(
            "Dokument aus dem Demo-Eingang",
            list(eingang_docs) or ["(keine Dokumente in demo/eingang/)"],
        )
    with col_up:
        uploaded = st.file_uploader(
            "… oder eigenes Markdown-Dokument", type=["md", "txt"]
        )

    if uploaded is not None:
        doc_path = EINGANG_DIR / f"upload-{uploaded.name}"
        doc_path.write_bytes(uploaded.getvalue())
    else:
        doc_path = eingang_docs.get(selected_name)

    if doc_path is not None:
        already_ingested = (CORPUS_DIR / doc_path.name).exists()
        if already_ingested:
            st.warning(
                f"`{doc_path.name}` wurde bereits eingespeist — `make reset` "
                f"stellt den Ausgangszustand wieder her."
            )
        with st.expander(f"Dokument ansehen: {doc_path.name}"):
            st.code(doc_path.read_text(encoding="utf-8")[:3000], language="markdown")

    go = st.button(
        "📥 In beide Systeme einspeisen",
        type="primary",
        disabled=doc_path is None or replay,
        help="Im Replay-Modus nicht verfügbar." if replay else None,
    )

    if go and doc_path is not None:
        left, right = st.columns(2)

        with left:
            st.subheader("🧩 RAG")
            st.caption("Zerschneiden, Embeddings, ablegen — mehr passiert nicht")
            with st.spinner("Indexiere …"):
                rag_stats = ingest_rag(doc_path)
            st.info(
                f"✅ Fertig in **{rag_stats['seconds']:.1f} s** "
                f"({rag_stats['chunks']} Chunks im Index).\n\n"
                f"Verknüpft: **nichts**. Widersprüche geprüft: **nein**. "
                f"Gelernt: **nichts** — das Dokument liegt jetzt einfach mit im Topf."
            )

        with right:
            st.subheader("📚 LLM-Wiki")
            st.caption("Der Ingest-Agent arbeitet das Dokument ins Wissensnetz ein")
            steps: list[str] = []
            steps_box = st.empty()
            icons = {"read": "📖 liest", "write": "✍️ **schreibt**"}

            def show_step(kind: str, rel: str) -> None:
                steps.append(f"{icons[kind]} `{rel}`")
                steps_box.markdown("\n".join(f"- {s}" for s in steps))

            try:
                with st.spinner("Agent liest und schreibt …"):
                    wiki_stats = ingest_wiki(doc_path, on_step=show_step)
            except Exception as exc:
                st.error(f"Fehler beim Ingest: {exc}")
            else:
                st.success(
                    f"✅ Fertig in **{wiki_stats['seconds']:.0f} s** — "
                    f"**{len(wiki_stats['pages'])} Seiten aktualisiert oder neu angelegt**, "
                    f"Querverweise gesetzt, Log geführt:\n\n"
                    + "\n".join(f"- `{p}`" for p in wiki_stats["pages"])
                )
                st.markdown(f"**Zusammenfassung des Agenten:** {wiki_stats['summary']}")
                st.caption(
                    "💬 Jetzt im Tab „Fragen stellen“ ausprobieren: "
                    "„Welche Vorfälle gab es 2026 …?“ (Akt 4)"
                )

# ═══════════════════════════════════════════════════════════════ Erklärung ═══
with tab_info:
    st.markdown(
        """
### Zwei Backends, dieselben Dokumente, dasselbe KI-Modell

Beide Systeme kennen exakt dieselben Quelldokumente (Ordner `corpus/`) und
nutzen für die Antwort dasselbe KI-Modell — der einzige Unterschied ist,
**wie das Wissen organisiert ist**.
"""
    )

    col_rag, col_wiki = st.columns(2)
    with col_rag:
        st.markdown(
            """
#### 🧩 RAG (links)

**Daten hinein** — vollautomatisch, Sekunden:
1. Dokument in ~900-Zeichen-Schnipsel zerschneiden
2. Jeden Schnipsel in einen Zahlencode übersetzen
   (Embeddings — lokal, kostenlos)
3. In der Vektor-Datenbank ablegen (`.chroma/`)

**Frage beantworten** — 1 KI-Aufruf:
1. Frage ebenfalls in Zahlencode übersetzen
2. Die 5 ähnlichsten Schnipsel heraussuchen
3. KI bekommt Schnipsel + Frage und antwortet

➡️ *Schnell und billig — aber niemand hat je geprüft,
was zusammengehört oder was noch aktuell ist.*
"""
        )
    with col_wiki:
        st.markdown(
            """
#### 📚 LLM-Wiki (rechts)

**Daten hinein** — ein KI-Agent pro Dokument (~2 min):
1. Agent liest das neue Dokument und die betroffenen
   Wiki-Seiten (`wiki/`)
2. Arbeitet Fakten ein, **klärt Widersprüche**, setzt
   Querverweise, legt neue Seiten an
3. Schreibt einen Eintrag ins Änderungs-Log (`log.md`)

**Frage beantworten** — Agent mit Werkzeugen:
1. Startet auf der Startseite `index.md`
2. Folgt gezielt den Links zu relevanten Seiten
3. Antwortet mit Quellen — und darf **Erkenntnisse als
   neue Wiki-Seite speichern**

➡️ *Wissen wird einmal einsortiert statt bei jeder
Frage neu zusammengeraten.*
"""
        )

    st.markdown(
        """
---
**Zum Nachschauen:** Rohdokumente in `corpus/`, das Wiki in `wiki/`
(einfach die Markdown-Dateien öffnen — z. B. `wiki/log.md`), der gesamte Code
in `app/` (wenige hundert Zeilen Python). Ausgangszustand wiederherstellen:
`make reset`. Details: `demo/drehbuch.md` und die Folien in `slides/`.
"""
    )

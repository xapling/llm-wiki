# RAG vs. LLM-Wiki — Showcase

Ein wiederholbares Demo-Projekt, das den Unterschied zwischen klassischem **RAG**
(Retrieval-Augmented Generation) und dem **LLM-Wiki-Muster**
([Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) bzw. dem
**Open Knowledge Format (OKF)**
([Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing))
sichtbar macht.

## Das Szenario

Die fiktive **SolarFlow GmbH** (B2B-SaaS für Photovoltaik-Monitoring) hat ~14 interne
Dokumente in [`corpus/`](corpus/): Meeting-Notizen, Architektur-Entscheidungen (ADRs),
Runbooks, Incident-Reports. Der Korpus enthält absichtlich eingebaute Fallen:

- **Multi-Hop-Wissen**: Warum Kunde Helios gekündigt hat, steht in keinem einzelnen Dokument.
- **Widersprüche**: Das Runbook nennt ein Rate-Limit von 100 req/min, ein späteres Meeting
  beschließt 500 req/min für Enterprise.
- **Aggregation**: "Welche Entscheidungen gelten noch?" erfordert Überblick über alle ADRs.

Dieselben Fragen laufen gegen zwei Backends:

| | RAG | LLM-Wiki (OKF) |
|---|---|---|
| Wissensbasis | Chunks + Embeddings (Chroma) | kuratiertes Markdown-Wiki ([`wiki/`](wiki/)) |
| Bei jeder Frage | Top-k-Chunks abrufen, neu herleiten | `index.md` navigieren, Konzeptseiten lesen |
| Neues Dokument | re-indexieren (nichts gelernt) | Ingest: Agent aktualisiert Wiki-Seiten + `log.md` |
| Widersprüche | landen beide im Kontext | beim Ingest aufgelöst und dokumentiert |
| Erkenntnisse aus Fragen | verworfen | können als neue Wiki-Seite gespeichert werden |

## Schnellstart

```bash
make setup      # venv + Abhängigkeiten
make reset      # Wiki aus seed/ herstellen + Vektor-Index bauen
make run        # Streamlit-UI (Side-by-Side-Vergleich)
```

Voraussetzung: `OPENROUTER_API_KEY` in `.env.local` (alle LLM-Aufrufe laufen
über OpenRouter mit einem einzigen Modell, siehe `MODEL` in [app/common.py](app/common.py)).

## Die Demo (siehe [demo/drehbuch.md](demo/drehbuch.md))

1. **Einfacher Lookup** — beide Backends antworten gut (RAG ist nicht schlecht!).
2. **Multi-Hop** — RAG antwortet lückenhaft, das Wiki hat die Synthese bereits.
3. **Widerspruch** — RAG liefert 100 *und* 500 req/min, das Wiki den aufgelösten Stand.
4. **Live-Ingest** — in der UI (Tab „Neues Dokument einspeisen") oder per
   `make ingest`: RAG re-indexiert stumpf, der Wiki-Agent aktualisiert sichtbar
   mehrere Seiten und `log.md`.
5. **Query wird Wissen** — eine Analyse-Frage, deren Antwort als neue Wiki-Seite landet.

## Wiederholbarkeit

- `make reset` stellt den Ausgangszustand her (Wiki aus `seed/wiki/`, Index neu,
  Ingest-Dokument entfernt) — die Demo ist beliebig oft identisch durchführbar.
- `make record` zeichnet die Antworten der Drehbuch-Fragen auf; der **Replay-Modus**
  in der UI spielt sie ohne API ab (Fallback bei WLAN-/API-Problemen im Termin).

## Struktur

```
corpus/         Rohdokumente (Source of Truth, unveränderlich)
seed/wiki/      Eingechecktes OKF-Bundle (Ausgangszustand)
wiki/           Arbeitskopie des Wikis (von `make reset` erzeugt, vom Agent gepflegt)
app/            RAG-Backend, Wiki-Agent, Ingest-Agent, Streamlit-UI
demo/           Drehbuch, Ingest-Eingangsdokument, Antwort-Cache
slides/         Theorieteil als Marp-Folien
```

## Folien

```bash
make slides     # rendert slides/praesentation.md nach slides/praesentation.html (braucht npx)
```

Aufbau des Theorieteils: **Problem → RAG als Lösung → Probleme mit RAG → LLM-Wiki → OKF → Demo.**

VENV := .venv
PY := $(VENV)/bin/python
INGEST_DOC := demo/eingang/2026-07-02-incident-api-gateway.md

.PHONY: setup reset index run ingest record slides clean

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r app/requirements.txt

## Ausgangszustand herstellen: Wiki aus seed/, eingespeiste Dokumente raus, Index neu
reset:
	rm -rf wiki
	cp -R seed/wiki wiki
	@for f in demo/eingang/*.md; do rm -f "corpus/$$(basename $$f)"; done
	rm -f demo/eingang/upload-*
	rm -rf .chroma
	$(PY) -m app.indexer
	@echo "\n✔ Reset abgeschlossen — Demo ist im Ausgangszustand."

index:
	$(PY) -m app.indexer

run:
	$(VENV)/bin/streamlit run app/ui.py

## Live-Ingest-Demo: neues Dokument in beide Welten einspeisen
ingest:
	$(PY) -m app.ingest $(INGEST_DOC)

## Drehbuch-Antworten aufzeichnen (Fallback für Replay-Modus)
record:
	$(PY) -m app.record

slides:
	npx --yes @marp-team/marp-cli --html slides/praesentation.md -o slides/praesentation.html

clean:
	rm -rf $(VENV) .chroma wiki __pycache__ app/__pycache__

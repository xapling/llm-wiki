# Demo-Drehbuch

Vor jedem Termin: `make reset` (stellt Wiki + Index in den Ausgangszustand).
Fallback ohne API/WLAN: Replay-Modus in der UI aktivieren (vorher einmal
`make record` ausführen).

Die fünf Akte eskalieren bewusst: erst zeigen, dass RAG funktioniert — dann,
wo es strukturell an Grenzen stößt.

---

## Akt 1 — Einfacher Lookup (beide gut)

> **Welchen Message-Broker setzen wir ein und wofür?**

Erwartung: Beide Backends antworten korrekt (Kafka, Entkopplung Ingest ↔
Datenhaltung, ADR-002). **Botschaft:** RAG ist nicht schlecht — für punktuelle
Fakten in einem einzelnen Dokument ist es völlig ausreichend.

## Akt 2 — Multi-Hop-Synthese (RAG lückenhaft)

> **Warum hat Helios Energie gekündigt? Erzähl die ganze Geschichte.**

Die Antwort verteilt sich auf drei Dokumente: Incident-Report (14.03.),
Kundenreview (20.03.), Sales-Quartalsreview (08.05.). RAG holt Top-k-Chunks und
erwischt typischerweise nur Teile der Kette; das Wiki hat auf
`kunden/helios-energie.md` die komplette, beim Ingest kompilierte Chronologie.
**Botschaft:** RAG *findet* Fragmente, das Wiki *kennt* den Zusammenhang.

## Akt 3 — Widerspruch (RAG verwirrt, Wiki aufgelöst)

> **Wie viele Requests pro Minute erlaubt unsere öffentliche API?**

Das Runbook (Nov 2025) sagt 100 req/min, das Platform-Weekly (April 2026)
beschließt 500 req/min für Enterprise. Beide Chunks landen bei RAG im Kontext —
bestenfalls nennt es beide Zahlen unkommentiert. Die Wiki-Seite
`systeme/api-gateway.md` dokumentiert den aufgelösten Stand inklusive des
Hinweises, dass das Runbook veraltet ist. **Botschaft:** Das Wiki hat den
Widerspruch beim Ingest *bemerkt und aufgelöst* — RAG kann das prinzipiell nicht.

## Akt 4 — Live-Ingest (der Höhepunkt)

In der UI auf den Tab **„📥 Neues Dokument einspeisen"** wechseln, den
Störungsbericht vom 02.07. auswählen (vorher kurz im Aufklapper zeigen) und
**„In beide Systeme einspeisen"** klicken:

- **Links (RAG):** nach Sekunden fertig — „Verknüpft: nichts. Gelernt: nichts."
- **Rechts (Wiki):** Der Agent liest und schreibt sichtbar Seite für Seite
  (API-Gateway, Vorfälle, Kunde Windkraft Nord entsteht neu, `log.md`),
  am Ende grüne Bilanz + Zusammenfassung des Agenten.

Dauert **~2 Minuten** — die Schritte laufen live rein, ideale Zeit zum
Kommentieren: „Er liest erst die Indizes … jetzt legt er die Kundenseite an,
die seit Mai vorgemerkt war … jetzt löst er die offene Pool-Sizing-Frage auf."

*(Alternativ im Terminal: `make ingest` — gleicher Ablauf als Konsolen-Ausgabe.
Man kann auch ein eigenes Markdown-Dokument hochladen.)*

Danach in der UI fragen:

> **Welche Vorfälle gab es 2026 und was waren jeweils die Ursachen?**

**Botschaft:** Beim Wiki ist Ingest *Integration*, bei RAG nur *Ablage*.

## Akt 5 — Query wird Wissen

> **Welche wiederkehrenden Muster erkennst du in unseren Vorfällen von 2026?**

Der Wiki-Agent analysiert (beide Vorfälle gehen auf nicht mitgezogene
Kapazitäts-/Konfigurationsgrenzen zurück, die vorher als Risiko dokumentiert
waren) und **speichert die Analyse als neue Seite** `analysen/incident-muster.md`.
Beim nächsten `make reset` ist sie wieder weg — beim echten Einsatz wäre sie
dauerhafter Wissensbestand. **Botschaft:** Erkenntnisse kumulieren, statt bei
jeder Frage neu hergeleitet (und verworfen) zu werden.

---

## Moderationshinweise

- Pro Akt zuerst die Frage vorlesen, dann Erwartung ansagen, dann ausführen.
- In der UI die Expander "Was hat das System gesehen?" öffnen — der Unterschied
  Chunks vs. Navigationspfad ist das stärkste visuelle Argument.
- Auf Token-/Latenz-Anzeigen hinweisen: Das Wiki liest gezielt wenige Seiten.
- Zum Abschluss `wiki/log.md` zeigen: die Historie des Wissensbestands.

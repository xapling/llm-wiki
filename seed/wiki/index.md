---
type: Index
title: SolarFlow Wissens-Wiki
description: Einstiegspunkt in das interne Wissens-Wiki der SolarFlow GmbH (OKF-Bundle).
tags: [index]
timestamp: 2026-06-15T09:00:00Z
---

# SolarFlow Wissens-Wiki

Dieses Wiki ist die kuratierte Wissensschicht über den Rohdokumenten in
`corpus/`. Es wird von einem LLM-Agenten gepflegt: Neue Quellen werden per
Ingest integriert, Widersprüche aufgelöst, Querverweise gesetzt. Änderungen
stehen in [log.md](/log.md).

**SolarFlow GmbH** ist ein B2B-SaaS für Photovoltaik-Monitoring (~40.000
Anlagen, Messintervall 5 Minuten). Teams: Platform (Miriam Osei), Produkt
(Jonas Brenner), Sales/CS (Leyla Aydin).

## Bereiche

- [Systeme](/systeme/index.md) — Architektur-Komponenten und ihr Betriebszustand
- [Entscheidungen](/entscheidungen/index.md) — ADRs mit aktuellem Gültigkeitsstatus
- [Kunden](/kunden/index.md) — Kundenseiten mit Historie und Vertragsstatus
- [Vorfälle](/vorfaelle/index.md) — Incidents mit Ursachen und Lehren
- [Produkt](/produkt/index.md) — Roadmap und Feature-Stand
- [Analysen](/analysen/index.md) — gespeicherte Erkenntnisse aus Anfragen

## Aktuell wichtig (Stand Juni 2026)

- Kündigung des größten Kunden [Helios Energie](/kunden/helios-energie.md)
  zum 30.09.2026 — Hintergründe dort.
- [TimescaleDB-Migration](/entscheidungen/adr-003-timescaledb.md) der Messdaten
  ist abgeschlossen.
- CSV-Export hat festen Liefertermin 15.08.2026, [Alerting v2 auf Q4
  verschoben](/produkt/roadmap-2026.md).

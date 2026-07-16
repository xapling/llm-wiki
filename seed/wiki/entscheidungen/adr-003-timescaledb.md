---
type: Entscheidung
title: ADR-003 — TimescaleDB für Messdaten
description: März 2026; Messdaten auf TimescaleDB, Stammdaten bleiben PostgreSQL. Umgesetzt.
tags: [entscheidungen, adr, datenbank, timescaledb]
timestamp: 2026-06-12T10:00:00Z
sources:
  - corpus/2026-03-05-adr-003-timescaledb-migration.md
  - corpus/2026-02-18-meeting-architektur-runde.md
  - corpus/2026-06-10-meeting-platform-weekly.md
---

# ADR-003 — TimescaleDB für Messdaten

**Status: ✅ gültig und umgesetzt** (Migration abgeschlossen 28.05.2026,
bestätigt im Platform-Weekly 10.06.2026).

- Datum: 05.03.2026 · Autor: Deniz Kaya · Ersetzt teilweise
  [ADR-001](/entscheidungen/adr-001-postgresql.md)
- Kern: Messdaten auf TimescaleDB (Hypertables, Compression ~90 %, Continuous
  Aggregates); Stammdaten bleiben in PostgreSQL.
- Vorarbeit: Architektur-Runde 18.02.2026 bewertete TimescaleDB, ClickHouse und
  InfluxDB. Ausschlaggebend für TimescaleDB: PostgreSQL-Extension — SQL,
  Tooling und Team-Wissen bleiben nutzbar; geringstes Betriebsrisiko neben dem
  Q2-Großprojekt Mandantenfähigkeit.

## Ergebnis

Dashboard-p95 für 30-Tage-Abfragen: 8,2 s → **0,9 s**. Details auf
[messdaten-speicher](/systeme/messdaten-speicher.md).

---
type: System
title: Messdaten-Speicher
description: TimescaleDB für Zeitreihen (seit Mai 2026), PostgreSQL für Stammdaten.
tags: [systeme, datenbank, betrieb]
timestamp: 2026-06-12T10:00:00Z
sources:
  - corpus/2025-02-10-adr-001-postgresql-messdaten.md
  - corpus/2026-02-18-meeting-architektur-runde.md
  - corpus/2026-03-05-adr-003-timescaledb-migration.md
  - corpus/2026-06-10-meeting-platform-weekly.md
---

# Messdaten-Speicher

## Aktueller Stand (seit 28.05.2026)

- **Messdaten (Zeitreihen): TimescaleDB** — Hypertables mit Compression und
  Continuous Aggregates. Entscheidung: [ADR-003](/entscheidungen/adr-003-timescaledb.md).
- **Stammdaten (Anlagen, Kunden, Verträge): PostgreSQL 16** — hier gilt
  [ADR-001](/entscheidungen/adr-001-postgresql.md) unverändert weiter.

Migration abgeschlossen (Platform-Weekly 10.06.2026): Doppelschreiben ab
07.04., Lesepfade seit 28.05. umgeschaltet. Wirkung: Dashboard-p95 für
30-Tage-Abfragen von 8,2 s auf **0,9 s**.

## Historie

- Feb 2025: ADR-001 — PostgreSQL für alles (damals 12 Mio. Punkte/Tag).
- Feb 2026: Architektur-Runde — bei 31 Mio. Punkten/Tag Symptome: langsame
  Dashboard-Abfragen, materialisierte Views laufen in den Vormittag,
  Vacuum-Probleme. Bewertet: TimescaleDB vs. ClickHouse vs. InfluxDB.
- März 2026: ADR-003 — TimescaleDB gewinnt (PostgreSQL-Extension: Team-Wissen
  und Tooling bleiben nutzbar).

## Abhängigkeiten

Gelesen von Dashboard und [API-Gateway](/systeme/api-gateway.md); befüllt über
den [Eventbus](/systeme/eventbus.md).

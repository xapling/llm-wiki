---
type: Entscheidung
title: ADR-001 — PostgreSQL als zentrale Datenbank
description: Feb 2025; ursprünglich für alle Daten, seit ADR-003 nur noch für Stammdaten gültig.
tags: [entscheidungen, adr, datenbank]
timestamp: 2026-03-08T09:00:00Z
sources:
  - corpus/2025-02-10-adr-001-postgresql-messdaten.md
  - corpus/2026-03-05-adr-003-timescaledb-migration.md
---

# ADR-001 — PostgreSQL als zentrale Datenbank

**Status: ⚠️ teilweise abgelöst durch [ADR-003](/entscheidungen/adr-003-timescaledb.md)
(März 2026).** Für Stammdaten gültig, für Messdaten nicht mehr.

- Datum: 10.02.2025 · Autor: Deniz Kaya
- Kern: PostgreSQL 16 für Stammdaten *und* Messdaten (partitionierte Tabelle
  `measurements`), begründet mit Team-Wissen und geringem Betriebsaufwand bei
  damals 12 Mio. Messpunkten/Tag.

## Warum die Ablösung kam

Der ADR benannte die Grenze selbst ("bei starkem Wachstum neu bewerten").
Bei 31 Mio. Punkten/Tag (Anfang 2026) traten die vorhergesagten Probleme ein —
Details auf [messdaten-speicher](/systeme/messdaten-speicher.md).

## Heute relevant

Für Anlagen-, Kunden- und Vertragsdaten ist PostgreSQL weiterhin die
festgelegte Datenbank.

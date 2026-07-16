---
type: Index
title: Systeme
description: Architektur-Komponenten der SolarFlow-Plattform mit Betriebszustand.
tags: [systeme, architektur]
timestamp: 2026-06-12T10:00:00Z
---

# Systeme

Datenfluss: Wechselrichter → [Ingest-Pipeline](/systeme/ingest-pipeline.md) →
[Eventbus](/systeme/eventbus.md) → [Messdaten-Speicher](/systeme/messdaten-speicher.md)
→ Dashboard / [API-Gateway](/systeme/api-gateway.md).

| Seite | Kurzbeschreibung |
|---|---|
| [ingest-pipeline](/systeme/ingest-pipeline.md) | Annahme der Wechselrichter-Messdaten |
| [eventbus](/systeme/eventbus.md) | Kafka, entkoppelt Ingest und Verarbeitung |
| [messdaten-speicher](/systeme/messdaten-speicher.md) | TimescaleDB (Messdaten) + PostgreSQL (Stammdaten) |
| [api-gateway](/systeme/api-gateway.md) | Öffentliche REST-API für Kunden-Integrationen |

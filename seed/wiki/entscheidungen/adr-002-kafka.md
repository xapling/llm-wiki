---
type: Entscheidung
title: ADR-002 — Apache Kafka als Eventbus
description: Juni 2025; Kafka entkoppelt Ingest und Datenhaltung. Gültig.
tags: [entscheidungen, adr, kafka]
timestamp: 2026-03-17T09:00:00Z
sources:
  - corpus/2025-06-20-adr-002-kafka-eventbus.md
  - corpus/2026-03-14-incident-ingest-ausfall.md
---

# ADR-002 — Apache Kafka als Eventbus

**Status: ✅ gültig.**

- Datum: 20.06.2025 · Autorin: Miriam Osei
- Kern: Kafka zwischen [Ingest-Pipeline](/systeme/ingest-pipeline.md) und
  Datenhaltung (Topic `measurements.raw`, 12 Partitionen, Retention 7 Tage),
  um Lastspitzen zu puffern und Reprocessing zu ermöglichen.

## Nachgeschichte

Das im ADR benannte Risiko "Disk-Sizing muss mit der Anlagenzahl mitwachsen"
wurde nicht operationalisiert und führte zum
[SEV-1-Vorfall am 14.03.2026](/vorfaelle/2026-03-14-ingest-ausfall.md).
Die Entscheidung für Kafka selbst steht nicht in Frage; die Lehre betrifft
Kapazitätsplanung als Prozess (seit April 2026 Quartals-Termin).

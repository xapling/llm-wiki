---
type: Vorfall
title: 14.03.2026 — Ausfall Ingest-Pipeline (SEV-1)
description: 6h15 Komplettausfall durch volle Kafka-Disk + kaputte Eskalationskette; SLA-Verletzung Helios.
tags: [vorfaelle, sev1, kafka, ingest]
timestamp: 2026-03-22T09:00:00Z
sources:
  - corpus/2026-03-14-incident-ingest-ausfall.md
  - corpus/2026-03-20-meeting-kundenreview-helios.md
---

# 14.03.2026 — Ausfall Ingest-Pipeline (SEV-1)

02:10–08:25 Uhr (6h15): [Ingest-Pipeline](/systeme/ingest-pipeline.md)
verarbeitete keine Messdaten; Datenlücke für alle Kunden.

## Ursachen

1. Volle Disk auf Kafka-Broker 2 ([Eventbus](/systeme/eventbus.md)) — das
   Disk-Sizing war seit Anfang 2025 nicht ans Wachstum (2,5×) angepasst.
   **Das Risiko war im Runbook und in [ADR-002](/entscheidungen/adr-002-kafka.md)
   dokumentiert, aber nie operationalisiert.**
2. Alarm feuerte um 02:14, erreichte aber niemanden — die On-Call-Eskalation
   zeigte auf einen veralteten Pager-Dienst. Entdeckt wurde der Ausfall vom
   Kunden (07:50).

## Wirkung

- Permanente Datenlücke bei ~15 % der Anlagen (Puffer der Wechselrichter
  reichte nicht).
- SLA-Verletzung bei [Helios Energie](/kunden/helios-energie.md) — Startpunkt
  der Kette, die zur Kündigung führte.

## Lehren / Maßnahmen

- Broker-Disk verdoppelt, Frühwarn-Alarm 60 % (✅ 20.03.)
- Eskalationskette umgestellt (✅ 18.03.)
- Kapazitätsplanung als Quartals-Termin (erstmals 01.07.2026)
- Proaktive Kundenkommunikation < 60 min bei SEV-1 (verbindlich seit Mai 2026)

**Muster-Kandidat:** dokumentiertes, aber nicht operationalisiertes
Kapazitätsrisiko. Bei künftigen Vorfällen prüfen, ob sich das wiederholt.

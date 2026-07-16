---
type: System
title: Eventbus (Kafka)
description: Apache Kafka entkoppelt Ingest-Pipeline und Datenhaltung; Topic measurements.raw.
tags: [systeme, kafka, betrieb]
timestamp: 2026-04-16T11:00:00Z
sources:
  - corpus/2025-06-20-adr-002-kafka-eventbus.md
  - corpus/2026-03-14-incident-ingest-ausfall.md
---

# Eventbus (Kafka)

Apache Kafka, eingeführt mit [ADR-002](/entscheidungen/adr-002-kafka.md)
(Juni 2025), entkoppelt die [Ingest-Pipeline](/systeme/ingest-pipeline.md) vom
[Messdaten-Speicher](/systeme/messdaten-speicher.md).

## Konfiguration

- Topic `measurements.raw`: 12 Partitionen, Retention 7 Tage
- Managed-Betrieb über den Cloud-Anbieter

## Betriebsgeschichte

Das in ADR-002 benannte Risiko "Disk-Sizing muss mitwachsen" ist am
**[14.03.2026 eingetreten](/vorfaelle/2026-03-14-ingest-ausfall.md)**: volle
Broker-Disk → 6h15 Ingest-Ausfall. Seitdem: Disk verdoppelt, Frühwarn-Alarm
bei 60 % (statt vorher 80 %).

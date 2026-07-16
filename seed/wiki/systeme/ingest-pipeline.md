---
type: System
title: Ingest-Pipeline
description: Nimmt Messdaten von ~40.000 Wechselrichtern entgegen und publiziert sie nach Kafka.
tags: [systeme, ingest, betrieb]
timestamp: 2026-04-16T11:00:00Z
sources:
  - corpus/2025-03-12-runbook-ingest-pipeline.md
  - corpus/2026-03-14-incident-ingest-ausfall.md
  - corpus/2026-04-14-meeting-platform-weekly.md
---

# Ingest-Pipeline

Nimmt Messdaten der Wechselrichter über HTTPS entgegen (`ingest.solarflow.io`),
validiert und publiziert sie in das Kafka-Topic `measurements.raw` auf dem
[Eventbus](/systeme/eventbus.md). Consumer schreiben von dort in den
[Messdaten-Speicher](/systeme/messdaten-speicher.md).

## Kennzahlen (Normalbetrieb)

- Durchsatz 8.000–12.000 Messpunkte/s in der Spitze; nach Netz-Wiederanläufen
  kurzzeitig bis zu 10× (Wechselrichter liefern gepufferte Daten nach).
- Consumer-Lag-Ziel: < 30 s.

## Betriebsgeschichte

- **[Vorfall 14.03.2026](/vorfaelle/2026-03-14-ingest-ausfall.md)**: 6h15
  Komplettausfall (SEV-1) durch volle Kafka-Broker-Disk + kaputte
  Eskalationskette. SLA-Verletzung bei [Helios Energie](/kunden/helios-energie.md).
- Seitdem (Stand April 2026): Broker-Disk verdoppelt, Frühwarn-Alarm bei 60 %,
  Eskalationskette auf neuen On-Call-Dienst umgestellt, Kapazitätsplanung als
  Quartals-Termin etabliert (erstmals 01.07.2026).

## Offene Risiken

- Dynamische Retention-Policy für Kafka in Prüfung (Priya, seit April 2026).

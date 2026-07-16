---
type: Log
title: Änderungshistorie
description: Chronologisches Log aller Ingest- und Pflege-Operationen an diesem Wiki.
tags: [log]
timestamp: 2026-06-15T09:00:00Z
---

# Änderungshistorie

Neueste Einträge oben. Format: Datum · Operation · Quelle · berührte Seiten.

## 2026-06-15 · Lint

Konsistenzprüfung über alle Seiten. Querverweise ergänzt zwischen
[Roadmap](/produkt/roadmap-2026.md) und [Helios](/kunden/helios-energie.md)
(CSV-Export-Priorisierung). Keine offenen Widersprüche.

## 2026-06-12 · Ingest: Protokoll Platform-Weekly 10.06.2026

Berührte Seiten: [messdaten-speicher](/systeme/messdaten-speicher.md)
(Migration abgeschlossen, p95 0,9 s), [adr-003](/entscheidungen/adr-003-timescaledb.md)
(Status: umgesetzt), [roadmap-2026](/produkt/roadmap-2026.md) (Alerting v2 → Q4),
[api-gateway](/systeme/api-gateway.md) (Hinweis Backfill Windkraft Nord).

## 2026-05-10 · Ingest: Protokoll Sales-Quartalsreview 08.05.2026

Berührte Seiten: [helios-energie](/kunden/helios-energie.md) (Kündigung
eingetragen, Ursachenkette vervollständigt), [roadmap-2026](/produkt/roadmap-2026.md)
(CSV-Export: fester Termin 15.08.), [index](/index.md) (Abschnitt "Aktuell wichtig").
Notiz: Neukunde Windkraft Nord ab 01.06. — Kundenseite wird beim nächsten
relevanten Dokument angelegt.

## 2026-04-16 · Ingest: Protokoll Platform-Weekly 14.04.2026

Berührte Seiten: [api-gateway](/systeme/api-gateway.md) — **Widerspruch erkannt
und aufgelöst**: Runbook (Nov 2025) nennt 100 req/min, Beschluss vom 14.04. setzt
500 req/min für Enterprise. Wiki dokumentiert beide Stände mit Gültigkeit;
Runbook-Aktualisierung steht laut Protokoll noch aus.
Außerdem: [messdaten-speicher](/systeme/messdaten-speicher.md) (Doppelschreiben
stabil), [ingest-pipeline](/systeme/ingest-pipeline.md) (Disk-Maßnahmen).

## 2026-03-22 · Ingest: Kundenreview Helios 20.03.2026

Berührte Seiten: [helios-energie](/kunden/helios-energie.md) (Eskalation,
CSV-Export-Forderung, Kündigungsrisiko hoch), [roadmap-2026](/produkt/roadmap-2026.md)
(Querverweis Helios-Nachfrage), [2026-03-14-ingest-ausfall](/vorfaelle/2026-03-14-ingest-ausfall.md)
(Kundenwirkung ergänzt).

## 2026-03-17 · Ingest: Incident-Report 14.03.2026

Neue Seite: [2026-03-14-ingest-ausfall](/vorfaelle/2026-03-14-ingest-ausfall.md).
Berührte Seiten: [ingest-pipeline](/systeme/ingest-pipeline.md),
[eventbus](/systeme/eventbus.md) (Disk-Risiko eingetreten),
[helios-energie](/kunden/helios-energie.md) (SLA-Verletzung).

## 2026-03-08 · Ingest: ADR-003 05.03.2026

Neue Seite: [adr-003](/entscheidungen/adr-003-timescaledb.md). Berührte Seiten:
[adr-001](/entscheidungen/adr-001-postgresql.md) (Status: teilweise abgelöst),
[messdaten-speicher](/systeme/messdaten-speicher.md),
[architektur-runde-Verweis in adr-003].

## 2026-02-20 · Ingest: Architektur-Runde 18.02.2026

Berührte Seiten: [messdaten-speicher](/systeme/messdaten-speicher.md)
(Performance-Symptome, Optionsbewertung).

## 2026-01-22 · Ingest: Produkt-Roadmap 2026

Neue Seite: [roadmap-2026](/produkt/roadmap-2026.md).

## 2025-11-06 · Ingest: Runbook API-Gateway

Neue Seite: [api-gateway](/systeme/api-gateway.md).

## 2025-09-04 · Ingest: Security-Richtlinie

Sicherheitsregeln in [index](/index.md) verlinkt; eigene Seite bewusst nicht
angelegt (Richtlinie ist selbst gut strukturiert; Quelle wird direkt referenziert).

## 2025-06-22 · Ingest: ADR-002 Kafka

Neue Seiten: [adr-002](/entscheidungen/adr-002-kafka.md), [eventbus](/systeme/eventbus.md).

## 2025-03-14 · Ingest: Runbook Ingest-Pipeline

Neue Seite: [ingest-pipeline](/systeme/ingest-pipeline.md).

## 2025-02-12 · Ingest: ADR-001 PostgreSQL

Neue Seiten: [adr-001](/entscheidungen/adr-001-postgresql.md),
[messdaten-speicher](/systeme/messdaten-speicher.md).

## 2025-01-17 · Initialer Aufbau

Wiki angelegt aus Onboarding-Handbuch: [index](/index.md), Bereichs-Indizes,
[helios-energie](/kunden/helios-energie.md).

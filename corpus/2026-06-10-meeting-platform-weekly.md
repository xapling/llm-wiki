# Protokoll: Platform-Weekly

Datum: 10.06.2026 · Anwesend: Miriam Osei, Deniz Kaya, Priya Sharma, Tom Vogel

## 1. TimescaleDB-Migration — Abschluss

Lesepfade seit 28.05. vollständig umgeschaltet, alte `measurements`-Partitionen
werden nach 30 Tagen Parallelbetrieb archiviert. Dashboard-p95 für
30-Tage-Abfragen: von 8,2 s auf 0,9 s. Migration gilt als **abgeschlossen**.

## 2. Onboarding Windkraft Nord

Seit 01.06. produktiv, 3.500 Anlagen angebunden. Deren Integrations-Team fährt
aktuell umfangreiche Abrufe über die öffentliche API (Backfill historischer
Daten). Bisher unauffällig; Tom behält die Gateway-Metriken im Blick.

## 3. Alerting v2 — Verschiebung

Alerting v2 (ursprünglich Q1-Roadmap) wird **auf Q4 verschoben**: Die
Mandantenfähigkeit (Q2) hat mehr Platform-Kapazität gebunden als geplant, und
der CSV-Export hat nach der Helios-Kündigung Vorrang (fester Termin 15.08.).
Jonas kommuniziert die Verschiebung an die betroffenen Kunden.

## 4. Sonstiges

- Quartals-Termin Kapazitätsplanung (Lehre aus dem März-Vorfall) erstmals am
  01.07. — Priya bereitet Kafka- und TimescaleDB-Wachstumsprognosen vor.

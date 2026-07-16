---
type: Kunde
title: Helios Energie GmbH
description: Größter Kunde (~9.000 Anlagen, ~18 % ARR); gekündigt zum 30.09.2026 nach Vorfall + fehlendem CSV-Export.
tags: [kunden, enterprise, churn]
timestamp: 2026-05-10T09:00:00Z
sources:
  - corpus/2025-01-15-onboarding-handbuch.md
  - corpus/2026-03-14-incident-ingest-ausfall.md
  - corpus/2026-03-20-meeting-kundenreview-helios.md
  - corpus/2026-05-08-meeting-sales-quartalsreview.md
---

# Helios Energie GmbH

Enterprise-Kunde seit Gründungszeit, ~9.000 PV-Anlagen, SLA 99,5 %
Monatsverfügbarkeit, ~18 % des ARR. Ansprechpartner: Robert Hellmann (Leiter
Betriebsführung), Sandra Wilke (IT).

**Status: Kündigung eingereicht am 05.05.2026, wirksam zum 30.09.2026.
Wechsel zu GreenMetrics.**

## Die Ursachenkette der Kündigung (kompiliert aus drei Quellen)

1. **14.03.2026 — [SEV-1-Vorfall](/vorfaelle/2026-03-14-ingest-ausfall.md):**
   6h15 Ingest-Ausfall, Datenlücke, SLA-Verletzung. Verschärfend: Helios
   entdeckte den Ausfall selbst und erfuhr die Ursache erst auf Nachfrage
   ("Wir zahlen für ein Monitoring-System — und mussten selbst monitoren, dass
   es ausgefallen ist"). Bei ~1.400 Helios-Anlagen ist die Datenlücke permanent
   — kritisch für deren Ertragsgutachten.
2. **20.03.2026 — Eskalationstermin:** Helios fordert SLA-Gutschrift (zugesagt)
   und das Vorziehen des seit über einem Jahr gewünschten **CSV-Exports**
   (laut [Roadmap](/produkt/roadmap-2026.md) erst Q3 2026). Das Vorziehen wurde
   am 11.04. von Produkt abgelehnt (Kapazität durch Mandantenfähigkeit gebunden)
   — Helios reagierte "sehr verstimmt". CS stufte das Kündigungsrisiko als
   hoch ein.
3. **05.05.2026 — Kündigung:** Genannte Gründe: der Vorfall *und vor allem die
   Kommunikation dabei*, sowie der weiterhin fehlende CSV-Export; die Ablehnung
   des Vorziehens war laut Hellmann "der letzte Anstoß".

## Konsequenzen bei SolarFlow

- CSV-Export neu priorisiert: fester Liefertermin **15.08.2026**.
- Proaktive Kundenkommunikation < 60 min bei SEV-1 ist verbindlicher Prozess.
- Rückgewinnung zum 30.09. gilt als unrealistisch, außer CSV-Export ist
  produktiv **und** deutliche Preisanpassung (Einschätzung CS).

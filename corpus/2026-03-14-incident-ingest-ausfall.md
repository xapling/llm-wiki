# Incident-Report: Ausfall der Ingest-Pipeline am 14.03.2026

Erstellt: 16.03.2026 · Autorin: Priya Sharma · Schweregrad: SEV-1

## Zusammenfassung

Am 14.03.2026 zwischen 02:10 und 08:25 Uhr (6 Stunden 15 Minuten) hat die
Ingest-Pipeline keine Messdaten verarbeitet. Für alle Kunden entstand eine
Datenlücke; bei der Helios Energie GmbH wurde das vertragliche SLA (99,5 %
Monatsverfügbarkeit) dadurch verletzt.

## Ablauf

- 02:10 — Kafka-Broker 2 meldet volle Disk; das Topic `measurements.raw` nimmt
  keine neuen Nachrichten mehr an. Die Ingest-Pipeline beantwortet Anfragen der
  Wechselrichter mit 5xx.
- 02:14 — Alarm `kafka_disk_usage` feuert. **Der Alarm ging unter, weil die
  On-Call-Eskalation auf einen veralteten Pager-Dienst zeigte.**
- 07:50 — Kunde Helios meldet fehlende Daten im Dashboard über den Support.
- 08:05 — On-Call beginnt Analyse, Disk-Erweiterung der Broker eingeleitet.
- 08:25 — Pipeline verarbeitet wieder; Nachlauf der gepufferten Daten bis 11:40.

## Ursachen

1. Disk-Sizing der Kafka-Broker war seit Anfang 2025 nicht an das Wachstum
   (2,5-fache Datenmenge) angepasst worden — ein im Runbook dokumentiertes,
   aber nicht umgesetztes Risiko.
2. Kaputte Eskalationskette: Alarm erreichte niemanden.

## Folgen

- Datenlücke 14.03. 02:10–08:25 für alle Kunden (Wechselrichter-Puffer konnten
  nur teilweise nachliefern; bei ca. 15 % der Anlagen ist die Lücke permanent).
- SLA-Verletzung bei Helios Energie (Enterprise-Vertrag) — Customer Success
  wurde erst um 09:30 informiert, Helios erfuhr die Ursache erst auf Nachfrage.

## Maßnahmen

- [x] Broker-Disk verdoppelt, Frühwarn-Alarm bei 60 % (erledigt 20.03.)
- [x] Eskalationskette auf neuen On-Call-Dienst umgestellt (erledigt 18.03.)
- [ ] Kapazitätsplanung als wiederkehrender Quartals-Termin
- [ ] Proaktive Kundenkommunikation bei SEV-1 innerhalb 60 Minuten (Prozess mit CS)

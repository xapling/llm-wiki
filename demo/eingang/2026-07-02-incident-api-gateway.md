# Incident-Report: Degradierung des API-Gateways am 02.07.2026

Erstellt: 03.07.2026 · Autor: Tom Vogel · Schweregrad: SEV-2

## Zusammenfassung

Am 02.07.2026 zwischen 09:40 und 11:55 Uhr (2 Stunden 15 Minuten) war die
öffentliche REST-API stark degradiert: p99-Latenz über 20 Sekunden, zeitweise
bis zu 40 % Fehlerrate (HTTP 503). Das Dashboard und die Ingest-Pipeline waren
nicht betroffen. Hauptbetroffener Kunde: Windkraft Nord GmbH, deren
Backfill-Integration in dieser Zeit abbrach.

## Ablauf

- 09:40 — Windkraft Nord startet einen parallelisierten Backfill historischer
  Daten und schöpft das seit April geltende Enterprise-Rate-Limit von
  500 req/min erstmals dauerhaft aus.
- 09:52 — Alarm `gateway_latency_p99` feuert; On-Call übernimmt sofort
  (Eskalationskette funktionierte — Lehre aus dem März umgesetzt).
- 10:05 — Ursache identifiziert: Die Connection-Pools des Gateways (20
  Verbindungen pro Replica) wurden bei der Rate-Limit-Erhöhung im April
  **nicht mitskaliert** — ein im Runbook dokumentiertes Risiko.
- 10:20 — Proaktive Information an Windkraft Nord durch Customer Success
  (innerhalb 60 Minuten, neuer Prozess eingehalten).
- 11:10 — Pool auf 60 Verbindungen pro Replica erhöht, zusätzliche Replica
  ausgerollt.
- 11:55 — Fehlerrate wieder normal; Windkraft Nord setzt Backfill fort.

## Ursachen

1. Bei der Rate-Limit-Erhöhung (Beschluss 14.04.2026) wurde die im Runbook
   vermerkte Abhängigkeit zum Connection-Pool-Sizing übersehen.
2. Das Runbook API-Gateway war zum Zeitpunkt des Vorfalls weiterhin auf dem
   Stand von November 2025 (Rate-Limit dort noch mit 100 req/min angegeben).

## Maßnahmen

- [x] Connection-Pool auf 60 Verbindungen pro Replica, 4. Replica (erledigt 02.07.)
- [x] Lasttest mit 500 req/min pro Key über 2 h (erledigt 04.07.)
- [ ] Runbook API-Gateway aktualisieren (Rate-Limits + Pool-Sizing)
- [ ] Konfigurations-Abhängigkeiten bei Beschlüssen künftig als Checkliste im
      Platform-Weekly (Ownerin: Miriam)

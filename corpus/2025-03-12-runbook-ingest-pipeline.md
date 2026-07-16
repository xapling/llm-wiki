# Runbook: Ingest-Pipeline

Stand: 12.03.2025 · Verantwortlich: Team Platform (On-Call-Rotation)

## Zweck

Die Ingest-Pipeline nimmt Messdaten der Wechselrichter über HTTPS entgegen
(Endpoint `ingest.solarflow.io`), validiert sie und publiziert sie in das
Kafka-Topic `measurements.raw`. Von dort schreiben Consumer in den
Messdaten-Speicher.

## Kennzahlen (Normalbetrieb)

- Durchsatz: ca. 8.000–12.000 Messpunkte/Sekunde in Spitzenzeiten (Mittag)
- Consumer-Lag: < 30 Sekunden
- Fehlerquote Validierung: < 0,1 %

## Alarme und Reaktionen

| Alarm | Bedeutung | Sofortmaßnahme |
|---|---|---|
| `ingest_5xx_rate` | Endpoint lehnt Anfragen ab | Pods prüfen, ggf. hochskalieren |
| `consumer_lag_high` | Verarbeitung hinkt hinterher | Consumer-Instanzen prüfen, Lag-Ursache in Grafana |
| `kafka_disk_usage` | Broker-Disk > 80 % | Retention prüfen, Disk erweitern — NICHT Topic löschen |

## Bekannte Risiken

- Nach großflächigen Netz-Wiederanläufen liefern Wechselrichter gepufferte Daten
  nach; der Durchsatz kann sich kurzzeitig verzehnfachen.
- Das Disk-Sizing der Kafka-Broker ist auf die Anlagenzahl von Anfang 2025
  ausgelegt und muss bei Wachstum nachgezogen werden.

## Eskalation

On-Call Platform → Miriam Osei → Geschäftsführung (bei SLA-relevanten Ausfällen
> 2 h ist Customer Success zu informieren, damit betroffene Enterprise-Kunden
proaktiv kontaktiert werden).

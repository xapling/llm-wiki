# Runbook: API-Gateway

Stand: 04.11.2025 · Verantwortlich: Team Platform

## Zweck

Das API-Gateway stellt die öffentliche REST-API (`api.solarflow.io/v1`) bereit,
über die Kunden Messdaten und Anlagen-Stammdaten in eigene Systeme integrieren.
Authentifizierung per API-Key, Autorisierung pro Mandant.

## Rate-Limiting

Pro API-Key gilt ein **Rate-Limit von 100 Requests pro Minute**. Überschreitungen
werden mit HTTP 429 beantwortet. Das Limit ist bewusst konservativ gewählt, um
die dahinterliegende Datenbank vor Abfrage-Stürmen zu schützen.

## Konfiguration

- Deployment: 3 Replicas hinter dem Load Balancer
- Connection-Pool zur Datenbank: 20 Verbindungen pro Replica
- Timeout Upstream: 10 Sekunden

## Alarme und Reaktionen

| Alarm | Bedeutung | Sofortmaßnahme |
|---|---|---|
| `gateway_latency_p99` | p99 > 2 s | Langsame Queries identifizieren (Tracing) |
| `gateway_429_rate` | Viele Rate-Limit-Treffer | Betroffenen Kunden identifizieren, CS informieren |
| `gateway_5xx_rate` | Fehlerrate erhöht | Upstream-Verbindungen und DB-Last prüfen |

## Bekannte Risiken

- Der Connection-Pool ist auf das Rate-Limit von 100 req/min abgestimmt. Änderungen
  am Rate-Limit erfordern eine Neubewertung des Pool-Sizings.

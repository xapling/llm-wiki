---
type: System
title: API-Gateway
description: Öffentliche REST-API (api.solarflow.io/v1); Rate-Limits 100 (Standard) / 500 (Enterprise) req/min.
tags: [systeme, api, betrieb]
timestamp: 2026-06-12T10:00:00Z
sources:
  - corpus/2025-11-04-runbook-api-gateway.md
  - corpus/2026-04-14-meeting-platform-weekly.md
  - corpus/2026-06-10-meeting-platform-weekly.md
---

# API-Gateway

Stellt die öffentliche REST-API (`api.solarflow.io/v1`) bereit, über die Kunden
Messdaten und Stammdaten integrieren. Auth per API-Key, Autorisierung pro
Mandant. Liest aus dem [Messdaten-Speicher](/systeme/messdaten-speicher.md).

## Rate-Limiting (aktueller Stand)

| Vertragstyp | Limit | gültig seit |
|---|---|---|
| Standard | 100 req/min | Beginn |
| **Enterprise** | **500 req/min** | **21.04.2026** (Beschluss Platform-Weekly 14.04.2026) |

> ⚠️ **Bekannter Dokumentations-Rückstand:** Das Runbook API-Gateway (Stand
> 04.11.2025) nennt noch pauschal 100 req/min. Die Aktualisierung steht laut
> Protokoll vom 14.04.2026 aus. Diese Wiki-Seite ist der aktuelle Stand.

Auslöser der Erhöhung: Enterprise-Integrationen (u. a. Windkraft Nord in der
Evaluierung) stießen regelmäßig an das alte Limit.

## Konfiguration

- 3 Replicas hinter dem Load Balancer
- Connection-Pool zur DB: 20 Verbindungen pro Replica
- Timeout Upstream: 10 s

## Bekannte Risiken

- Das Runbook vermerkt: Der Connection-Pool ist auf das *alte* Limit von
  100 req/min abgestimmt; Änderungen am Rate-Limit erfordern eine Neubewertung
  des Pool-Sizings. **Ob das Pool-Sizing nach der Erhöhung auf 500 req/min
  angepasst wurde, ist nicht dokumentiert.**
- Seit Juni 2026 fährt der Neukunde Windkraft Nord umfangreiche Backfill-Abrufe
  über die API (Platform-Weekly 10.06.); Gateway-Metriken werden beobachtet (Tom).
  *(Kundenseite für Windkraft Nord existiert noch nicht — anlegen, sobald ein
  substanzielles Dokument eingeht.)*

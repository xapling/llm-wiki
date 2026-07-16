# Onboarding-Handbuch SolarFlow GmbH

Stand: 15.01.2025 · Autorin: Miriam Osei (Head of Platform)

Willkommen bei SolarFlow! Wir bauen eine B2B-SaaS-Plattform für das Monitoring von
Photovoltaik-Anlagen. Unsere Kunden sind Energieversorger und Betreiber großer
PV-Parks, die über unsere Plattform Erträge, Störungen und Wartungsbedarf ihrer
Anlagen im Blick behalten.

## Teams

- **Platform** (Miriam Osei): Ingest-Pipeline, Eventbus, Datenhaltung, API-Gateway
- **Produkt** (Jonas Brenner): Dashboard, Alerting, Reporting
- **Sales & Customer Success** (Leyla Aydin): Kundenbetreuung, Verträge, SLAs

## Systemlandschaft (Überblick)

1. **Ingest-Pipeline** — nimmt Messdaten der Wechselrichter entgegen (ca. 40.000
   Anlagen, Messintervall 5 Minuten) und schreibt sie über den Eventbus in den
   Messdaten-Speicher.
2. **Eventbus** — entkoppelt Ingest und Verarbeitung.
3. **Messdaten-Speicher** — zentrale Datenbank für Zeitreihen und Stammdaten.
4. **API-Gateway** — öffentliche REST-API für Kunden-Integrationen.
5. **Dashboard** — Web-Frontend für Endanwender.

## Wichtige Kunden

Unser größter Kunde ist die **Helios Energie GmbH** (rund 9.000 Anlagen, Enterprise-
Vertrag mit SLA 99,5 % Verfügbarkeit). Daneben betreuen wir u. a. die **Stadtwerke
Grünfeld** und mehrere mittelgroße Betreiber.

## Arbeitsweise

Architektur-Entscheidungen dokumentieren wir als ADRs (Architecture Decision
Records). Betriebswissen liegt in Runbooks. Meetings werden protokolliert und im
Wiki-Ordner abgelegt. Bei Vorfällen schreiben wir innerhalb von 48 Stunden einen
Incident-Report mit Ursachenanalyse.

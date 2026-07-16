# Protokoll: Platform-Weekly

Datum: 14.04.2026 · Anwesend: Miriam Osei, Deniz Kaya, Priya Sharma, Tom Vogel

## 1. TimescaleDB-Migration (ADR-003)

Doppelschreiben läuft seit 07.04. stabil. Abweichungen zwischen alter und neuer
Schreibstrecke < 0,01 %. Umschalten der Lesepfade für das Dashboard geplant für
KW 21.

## 2. Rate-Limit der öffentlichen API — Beschluss

Mehrere Enterprise-Kunden (u. a. Windkraft Nord in der Evaluierung) stoßen mit
ihren Integrationen regelmäßig an das Limit von 100 req/min. Nach Prüfung der
DB-Last durch Deniz:

**Beschluss: Das Rate-Limit wird für Enterprise-Verträge auf 500 Requests pro
Minute erhöht.** Für Standard-Verträge bleibt es bei 100 req/min. Umsetzung durch
Tom bis 21.04. Das Runbook API-Gateway ist entsprechend zu aktualisieren.
*(Anmerkung: Aktualisierung des Runbooks steht noch aus.)*

## 3. Kafka-Disk-Sizing

Nach dem Vorfall vom 14.03. wurde die Broker-Disk verdoppelt und ein
Frühwarn-Alarm bei 60 % eingerichtet. Priya prüft zusätzlich eine dynamische
Retention-Policy.

## 4. Sonstiges

- Onboarding neuer Engineer (Start 01.05.) — Miriam übernimmt Buddy-Rolle.
- Reminder: Incident-Reports bitte innerhalb 48 h finalisieren.

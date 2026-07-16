# Protokoll: Architektur-Runde — Zukunft des Messdaten-Speichers

Datum: 18.02.2026 · Anwesend: Miriam Osei, Deniz Kaya, Priya Sharma, Tom Vogel,
Jonas Brenner (Gast, Produkt-Sicht)

## Problemstellung

Das Datenvolumen ist seit ADR-001 um Faktor 2,5 gewachsen (aktuell 31 Mio.
Messpunkte/Tag). Symptome:

- Dashboard-Abfragen über 30 Tage: p95 bei 8,2 s (Ziel: < 2 s)
- Nächtliche materialisierte Views laufen bis ~10:30 Uhr in den Geschäftstag
- Vacuum/Autovacuum auf der `measurements`-Tabelle zunehmend problematisch

## Bewertete Optionen

| Option | Pro | Contra |
|---|---|---|
| **TimescaleDB** | PostgreSQL-Extension: SQL, Tooling, Team-Wissen bleiben; Continuous Aggregates; Compression | Single-Node-Grenzen langfristig |
| **ClickHouse** | Beste Abfrage-Performance für Analytik | neues System, neues Betriebs-Know-how, eigenes SQL-Dialekt |
| **InfluxDB** | etabliert für Zeitreihen | Flux-Sprache, Team-Skepsis, Lizenzmodell |

## Diskussion

Deniz präferiert TimescaleDB (geringstes Betriebsrisiko), Tom sieht ClickHouse
langfristig als leistungsfähiger, räumt aber ein, dass das Team dafür heute
nicht aufgestellt ist. Jonas betont aus Produkt-Sicht: Die Q2-Mandantenfähigkeit
darf nicht durch ein DB-Großprojekt gefährdet werden.

## Ergebnis

Konsens-Empfehlung an die Entscheidung (wird als ADR-003 ausgearbeitet):
**TimescaleDB für Messdaten, Stammdaten bleiben in PostgreSQL.** Deniz schreibt
den ADR-Entwurf bis Anfang März.

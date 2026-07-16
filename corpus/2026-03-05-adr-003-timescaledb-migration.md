# ADR-003: Migration der Messdaten auf TimescaleDB

Datum: 05.03.2026 · Status: Akzeptiert · Autor: Deniz Kaya (Platform)
Ersetzt teilweise: ADR-001

## Kontext

Seit ADR-001 (Februar 2025) haben sich die Rahmenbedingungen geändert: Wir sind
von 12 auf 31 Mio. Messpunkte pro Tag gewachsen. Die partitionierte
`measurements`-Tabelle in PostgreSQL stößt an Grenzen: Dashboard-Abfragen über
30-Tage-Zeiträume dauern teils über 8 Sekunden, die nächtlichen materialisierten
Views laufen bis in den Vormittag. Die Architektur-Runde vom 18.02.2026 hat
Alternativen bewertet (TimescaleDB, ClickHouse, InfluxDB).

## Entscheidung

Die **Messdaten werden auf TimescaleDB migriert** (Hypertables mit Compression
und Continuous Aggregates). **Stammdaten (Anlagen, Kunden, Verträge) bleiben in
PostgreSQL** — ADR-001 gilt für Stammdaten unverändert weiter, ist für Messdaten
aber abgelöst.

## Begründung

- TimescaleDB ist eine PostgreSQL-Extension: SQL, Tooling und Team-Wissen bleiben
  nutzbar (wichtigstes Kriterium gegenüber ClickHouse).
- Continuous Aggregates ersetzen die fragilen nächtlichen materialisierten Views.
- Compression reduziert den Speicherbedarf der Zeitreihen um ca. 90 %.

## Konsequenzen

- Migration in zwei Phasen: Doppelschreiben ab April 2026, Umschalten der
  Lesepfade bis Ende Q2 2026.
- Das Backup-Konzept muss um die TimescaleDB-Instanz erweitert werden.

# ADR-001: PostgreSQL als zentrale Datenbank

Datum: 10.02.2025 · Status: Akzeptiert · Autor: Deniz Kaya (Platform)

## Kontext

Wir brauchen eine Datenbank für Stammdaten (Anlagen, Kunden, Verträge) und für die
Messdaten der Wechselrichter (Zeitreihen, aktuell ca. 12 Mio. Datenpunkte pro Tag).
Das Team kennt PostgreSQL gut, wir wollen die Zahl der Technologien klein halten.

## Entscheidung

Wir verwenden **PostgreSQL 16 für alle Daten** — sowohl Stammdaten als auch
Messdaten. Die Messdaten liegen in einer partitionierten Tabelle
`measurements` (Partitionierung nach Monat).

## Begründung

- Ein System für alles: weniger Betriebsaufwand, ein Backup-Konzept.
- Team-Erfahrung: alle Platform-Engineers kennen PostgreSQL.
- Für das aktuelle Datenvolumen (12 Mio. Punkte/Tag) reicht die Performance mit
  Partitionierung nachweislich aus (Lasttest vom 03.02.2025).

## Konsequenzen

- Bei starkem Wachstum der Anlagenzahl müssen wir die Partitionierungsstrategie
  und ggf. eine spezialisierte Zeitreihen-Lösung neu bewerten.
- Aggregations-Abfragen über lange Zeiträume (> 1 Jahr) sind teuer und werden
  über nächtlich materialisierte Views abgefedert.

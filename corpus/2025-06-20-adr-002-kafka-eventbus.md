# ADR-002: Apache Kafka als Eventbus

Datum: 20.06.2025 · Status: Akzeptiert · Autorin: Miriam Osei (Platform)

## Kontext

Die Ingest-Pipeline schrieb bisher synchron in die Datenbank. Bei Lastspitzen
(z. B. nach Netz-Wiederanläufen, wenn zehntausende Wechselrichter gleichzeitig
gepufferte Daten nachliefern) kam es zu Timeouts und Datenverlust.

## Entscheidung

Wir führen **Apache Kafka** als Eventbus zwischen Ingest-Pipeline und
Datenhaltung ein. Die Ingest-Pipeline schreibt Messdaten in das Topic
`measurements.raw` (12 Partitionen, Retention 7 Tage), Consumer schreiben von
dort in die Datenbank.

## Begründung

- Entkopplung: Lastspitzen werden im Topic gepuffert statt die DB zu überlasten.
- Wiederverarbeitung: Bei Fehlern in Consumern können wir Offsets zurücksetzen.
- Kafka ist Industriestandard; Managed-Betrieb über unseren Cloud-Anbieter.

## Konsequenzen

- Neue Betriebsverantwortung: Topic-Konfiguration, Consumer-Lag-Monitoring.
- Die Retention von 7 Tagen begrenzt, wie weit wir zurück reprocessen können.
- Disk-Sizing der Broker muss mit der Anlagenzahl mitwachsen (siehe Runbook
  Ingest-Pipeline).

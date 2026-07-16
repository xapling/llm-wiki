# Security-Richtlinie (Auszug für Engineering)

Stand: 02.09.2025 · Verantwortlich: Miriam Osei (interimistisch, bis CISO-Rolle besetzt)

## Zugriff und Authentifizierung

- Zugriff auf Produktionssysteme nur über SSO mit MFA; keine geteilten Accounts.
- API-Keys der Kunden werden gehasht gespeichert und sind rotierbar; Kunden
  werden bei Verdacht auf Kompromittierung proaktiv informiert.
- Interne Service-zu-Service-Kommunikation über mTLS.

## Datenhaltung

- Messdaten und Stammdaten liegen ausschließlich in EU-Rechenzentren
  (Frankfurt, Region eu-central).
- Personenbezogene Daten (Ansprechpartner der Kunden) unterliegen der
  DSGVO-Löschfrist: 90 Tage nach Vertragsende.
- Backups: täglich, verschlüsselt, Aufbewahrung 35 Tage.

## Entwicklung

- Secrets niemals im Code oder in Tickets; ausschließlich im Secret-Manager.
- Dependency-Scanning im CI ist verpflichtend; kritische CVEs blockieren den Merge.
- Externe Penetrationstests jährlich (zuletzt: Juli 2025, keine kritischen Funde).

## Vorfälle

Sicherheitsvorfälle sind unverzüglich an Miriam zu melden und folgen dem
gleichen Incident-Prozess wie Betriebsvorfälle (Report innerhalb 48 h),
zusätzlich Prüfung der DSGVO-Meldepflicht (72 h).

---
marp: true
theme: default
paginate: true
html: true
style: |
  section {
    font-size: 30px;
    background: #FDFBF6;
    color: #2A3138;
  }
  h1 { font-size: 46px; color: #14466B; }
  h2 { font-size: 40px; color: #14466B; }
  h3 { color: #46586A; }
  strong { color: #B4551D; }
  a { color: #B4551D; }
  table { font-size: 26px; margin-left: auto; margin-right: auto; }
  th { background: #EDE7DA; color: #2A3138; }
  td { background: #FFFFFF; }
  code { background: #F1ECE1; color: #4A3B2A; }
  pre { background: #F6F2E9; border: 1px solid #E4DCCB; }
  pre code { background: transparent; color: #3C4650; }
  blockquote {
    border-left: 4px solid #C98A54;
    padding-left: 1em;
    color: #5C6670;
    background: #F8F3EA;
  }
  section::after { color: #9AA3AC; }
  svg.diagram { display: block; margin: 0.4em auto; }
  p.center { text-align: center; }
  .cols { display: flex; gap: 1.4em; align-items: flex-start; }
  .cols > div { flex: 1; min-width: 0; }
  .cols pre { font-size: 0.62em; margin: 0; }
  .cols p { font-size: 0.78em; margin: 0.5em 0; }
---

# Vom Suchen zum Wissen

## Wie eine KI unser Firmenwissen wirklich kennenlernt

<svg class="diagram" width="700" viewBox="0 0 700 110" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="240" height="70" rx="12" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="140" y="55" text-anchor="middle" font-size="26">🔍 RAG</text>
  <text x="140" y="80" text-anchor="middle" font-size="16" fill="#5C6670">heute üblich</text>
  <path d="M 280 55 H 400" stroke="#B4551D" stroke-width="4" fill="none"/>
  <polygon points="400,45 420,55 400,65" fill="#B4551D"/>
  <rect x="440" y="20" width="240" height="70" rx="12" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="560" y="55" text-anchor="middle" font-size="26">📚 LLM-Wiki</text>
  <text x="560" y="80" text-anchor="middle" font-size="16" fill="#5C6670">die neue Idee</text>
</svg>

<p class="center">Erst kurz die Idee (~15 min) — dann live ausprobieren (~15 min)</p>

---

## 1 · Das Problem: Die KI kennt unsere Firma nicht

<svg class="diagram" width="1000" viewBox="0 0 1000 340" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="90" width="220" height="160" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="150" y="170" text-anchor="middle" font-size="64">🤖</text>
  <text x="150" y="220" text-anchor="middle" font-size="22" fill="#14466B" font-weight="bold">Die KI</text>
  <text x="435" y="180" text-anchor="middle" font-size="60" fill="#B4551D" font-weight="bold">?</text>
  <rect x="560" y="30" width="400" height="70" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="760" y="72" text-anchor="middle" font-size="22">Warum hat unser Kunde gekündigt?</text>
  <rect x="560" y="130" width="400" height="70" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="760" y="172" text-anchor="middle" font-size="22">Welche Entscheidungen gelten noch?</text>
  <rect x="560" y="230" width="400" height="70" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="760" y="272" text-anchor="middle" font-size="22">Wie lief die Störung im März?</text>
</svg>

Die KI weiß viel über die Welt — aber **nichts über uns**.

---

## Und unser Wissen? Liegt überall verstreut.

<svg class="diagram" width="1000" viewBox="0 0 1000 330" xmlns="http://www.w3.org/2000/svg">
  <rect x="60" y="40" width="240" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="180" y="95" text-anchor="middle" font-size="24">📄 Wiki-Seiten</text>
  <rect x="390" y="90" width="240" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2" transform="rotate(-3 510 135)"/>
  <text x="510" y="145" text-anchor="middle" font-size="24" transform="rotate(-3 510 135)">🎫 Tickets</text>
  <rect x="710" y="45" width="240" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2" transform="rotate(2 830 90)"/>
  <text x="830" y="100" text-anchor="middle" font-size="24" transform="rotate(2 830 90)">📋 Protokolle</text>
  <rect x="200" y="190" width="240" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2" transform="rotate(3 320 235)"/>
  <text x="320" y="245" text-anchor="middle" font-size="24" transform="rotate(3 320 235)">📧 E-Mails</text>
  <rect x="560" y="200" width="240" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="680" y="255" text-anchor="middle" font-size="24">🗣️ In Köpfen</text>
  <g transform="rotate(-12 180 80)">
    <rect x="110" y="62" width="140" height="36" rx="6" fill="none" stroke="#B4551D" stroke-width="3"/>
    <text x="180" y="88" text-anchor="middle" font-size="20" fill="#B4551D" font-weight="bold">VERALTET</text>
  </g>
</svg>

Vieles ist doppelt, manches **veraltet** — und niemand hat den Überblick.

---

## 2 · Die übliche Lösung: RAG

<svg class="diagram" width="1050" viewBox="0 0 1050 380" xmlns="http://www.w3.org/2000/svg">
  <text x="30" y="45" font-size="22" fill="#5C6670" font-weight="bold">Einmal vorbereiten:</text>
  <rect x="30" y="70" width="260" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="160" y="112" text-anchor="middle" font-size="24">📄 Alle Dokumente</text>
  <text x="160" y="140" text-anchor="middle" font-size="18" fill="#5C6670">Wiki, Protokolle, …</text>
  <path d="M 300 115 H 370" stroke="#14466B" stroke-width="3"/><polygon points="370,107 386,115 370,123" fill="#14466B"/>
  <rect x="396" y="70" width="260" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="526" y="112" text-anchor="middle" font-size="24">✂️ Klein schneiden</text>
  <text x="526" y="140" text-anchor="middle" font-size="18" fill="#5C6670">in „Schnipsel“</text>
  <path d="M 666 115 H 736" stroke="#14466B" stroke-width="3"/><polygon points="736,107 752,115 736,123" fill="#14466B"/>
  <rect x="762" y="70" width="260" height="90" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="892" y="112" text-anchor="middle" font-size="24">🗄️ In eine Datenbank</text>
  <text x="892" y="140" text-anchor="middle" font-size="18" fill="#5C6670">durchsuchbar ablegen</text>
  <text x="30" y="235" font-size="22" fill="#5C6670" font-weight="bold">Bei jeder Frage:</text>
  <rect x="30" y="260" width="260" height="90" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="160" y="302" text-anchor="middle" font-size="24">❓ Frage stellen</text>
  <path d="M 300 305 H 370" stroke="#B4551D" stroke-width="3"/><polygon points="370,297 386,305 370,313" fill="#B4551D"/>
  <rect x="396" y="260" width="260" height="90" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="526" y="295" text-anchor="middle" font-size="24">🔍 Passende Schnipsel</text>
  <text x="526" y="325" text-anchor="middle" font-size="24">heraussuchen</text>
  <path d="M 666 305 H 736" stroke="#B4551D" stroke-width="3"/><polygon points="736,297 752,305 736,313" fill="#B4551D"/>
  <rect x="762" y="260" width="260" height="90" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="892" y="295" text-anchor="middle" font-size="24">🤖 KI liest sie</text>
  <text x="892" y="325" text-anchor="middle" font-size="24">und antwortet</text>
</svg>

**RAG** heißt: Die KI bekommt zu jeder Frage die passenden Text-Schnipsel.

---

## RAG kann viel — und ist zu Recht Standard

<svg class="diagram" width="1000" viewBox="0 0 1000 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="290" height="220" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="175" y="95" text-anchor="middle" font-size="48">✅</text>
  <text x="175" y="150" text-anchor="middle" font-size="24" font-weight="bold" fill="#14466B">Fakten finden</text>
  <text x="175" y="190" text-anchor="middle" font-size="18" fill="#5C6670">„Welche Datenbank</text>
  <text x="175" y="216" text-anchor="middle" font-size="18" fill="#5C6670">nutzen wir?“</text>
  <rect x="355" y="30" width="290" height="220" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="500" y="95" text-anchor="middle" font-size="48">✅</text>
  <text x="500" y="150" text-anchor="middle" font-size="24" font-weight="bold" fill="#14466B">Riesige Mengen</text>
  <text x="500" y="190" text-anchor="middle" font-size="18" fill="#5C6670">Millionen Dokumente?</text>
  <text x="500" y="216" text-anchor="middle" font-size="18" fill="#5C6670">Kein Problem.</text>
  <rect x="680" y="30" width="290" height="220" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="825" y="95" text-anchor="middle" font-size="48">✅</text>
  <text x="825" y="150" text-anchor="middle" font-size="24" font-weight="bold" fill="#14466B">Immer aktuell</text>
  <text x="825" y="190" text-anchor="middle" font-size="18" fill="#5C6670">Neues Dokument?</text>
  <text x="825" y="216" text-anchor="middle" font-size="18" fill="#5C6670">In Sekunden drin.</text>
</svg>

Das sehen wir gleich in der Demo: **Bei einfachen Fragen gewinnt niemand.**

---

## Schwäche 1: Schnipsel erzählen keine Geschichte

<svg class="diagram" width="1000" viewBox="0 0 1000 330" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="20" width="500" height="60" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="500" y="58" text-anchor="middle" font-size="23" font-weight="bold">❓ Warum hat der Kunde gekündigt?</text>
  <rect x="60" y="150" width="260" height="110" rx="14" fill="#FFFFFF" stroke="#4C7A3F" stroke-width="3"/>
  <text x="190" y="195" text-anchor="middle" font-size="22">📄 Störung im März</text>
  <text x="190" y="230" text-anchor="middle" font-size="19" fill="#4C7A3F" font-weight="bold">✓ gefunden</text>
  <rect x="370" y="150" width="260" height="110" rx="14" fill="#FDFBF6" stroke="#B0AA9C" stroke-width="2" stroke-dasharray="8 6"/>
  <text x="500" y="195" text-anchor="middle" font-size="22" fill="#8A8578">📄 Beschwerde-Termin</text>
  <text x="500" y="230" text-anchor="middle" font-size="19" fill="#B4551D" font-weight="bold">✗ nicht gefunden</text>
  <rect x="680" y="150" width="260" height="110" rx="14" fill="#FFFFFF" stroke="#4C7A3F" stroke-width="3"/>
  <text x="810" y="195" text-anchor="middle" font-size="22">📄 Kündigung im Mai</text>
  <text x="810" y="230" text-anchor="middle" font-size="19" fill="#4C7A3F" font-weight="bold">✓ gefunden</text>
  <text x="500" y="310" text-anchor="middle" font-size="22" fill="#5C6670">Eine Geschichte — verteilt auf drei Dokumente</text>
</svg>

Die Antwort steht in **keinem einzelnen Dokument**. RAG findet nur Teile davon.

---

## Schwäche 2: Widersprüche fallen nicht auf

<svg class="diagram" width="1000" viewBox="0 0 1000 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="60" y="40" width="320" height="110" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="220" y="80" text-anchor="middle" font-size="20" fill="#5C6670">📄 Handbuch · Nov 2025</text>
  <text x="220" y="120" text-anchor="middle" font-size="26" font-weight="bold">„100 Anfragen/Minute“</text>
  <rect x="60" y="180" width="320" height="110" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="220" y="220" text-anchor="middle" font-size="20" fill="#5C6670">📄 Protokoll · April 2026</text>
  <text x="220" y="260" text-anchor="middle" font-size="26" font-weight="bold">„500 Anfragen/Minute“</text>
  <path d="M 400 95 C 500 95 520 150 580 160" stroke="#14466B" stroke-width="3" fill="none"/>
  <path d="M 400 235 C 500 235 520 180 580 172" stroke="#14466B" stroke-width="3" fill="none"/>
  <polygon points="578,152 596,166 576,180" fill="#14466B"/>
  <rect x="610" y="100" width="330" height="140" rx="16" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="775" y="160" text-anchor="middle" font-size="52">🤖</text>
  <text x="775" y="212" text-anchor="middle" font-size="24" fill="#B4551D" font-weight="bold">„Was stimmt denn nun?“</text>
</svg>

Beide Schnipsel landen bei der KI — **niemand hat den Widerspruch geklärt**.

---

## Schwäche 3: Nichts bleibt hängen

<svg class="diagram" width="900" viewBox="0 0 900 330" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="120" width="180" height="80" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="130" y="168" text-anchor="middle" font-size="23">❓ Frage</text>
  <path d="M 232 160 H 292" stroke="#14466B" stroke-width="3"/><polygon points="292,152 308,160 292,168" fill="#14466B"/>
  <rect x="318" y="120" width="220" height="80" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="428" y="168" text-anchor="middle" font-size="23">🔍 Suchen & Denken</text>
  <path d="M 550 160 H 610" stroke="#14466B" stroke-width="3"/><polygon points="610,152 626,160 610,168" fill="#14466B"/>
  <rect x="636" y="120" width="200" height="80" rx="14" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="736" y="168" text-anchor="middle" font-size="23">💬 Antwort</text>
  <path d="M 736 212 C 736 305 480 322 268 296" stroke="#B4551D" stroke-width="3" fill="none" stroke-dasharray="9 7"/>
  <polygon points="276,286 256,296 274,306" fill="#B4551D"/>
  <text x="490" y="252" text-anchor="middle" font-size="24" fill="#B4551D" font-weight="bold">🗑️ … und alles wird wieder vergessen</text>
  <text x="130" y="290" text-anchor="middle" font-size="21" fill="#5C6670">nächste Frage:</text>
  <text x="130" y="318" text-anchor="middle" font-size="21" fill="#5C6670">wieder bei null</text>
</svg>

Jede gute Antwort kostet Arbeit — und wird danach **weggeworfen**.

---

## 3 · Die Idee: Die KI führt ein eigenes Wiki

Die Idee stammt von **Andrej Karpathy**, einem der bekanntesten KI-Forscher (Mitgründer von OpenAI, davor KI-Chef bei Tesla):

<svg class="diagram" width="760" viewBox="0 0 950 360" xmlns="http://www.w3.org/2000/svg">
  <rect x="120" y="30" width="710" height="70" rx="12" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="475" y="73" text-anchor="middle" font-size="22">📖 Spielregeln — wie das Wiki aufgebaut und gepflegt wird</text>
  <rect x="120" y="130" width="710" height="90" rx="12" fill="#FFFFFF" stroke="#B4551D" stroke-width="3"/>
  <text x="475" y="170" text-anchor="middle" font-size="25" font-weight="bold" fill="#14466B">📚 Das Wiki — von der KI geschrieben und gepflegt</text>
  <text x="475" y="202" text-anchor="middle" font-size="19" fill="#5C6670">Übersichten, Zusammenfassungen, Querverweise, Änderungs-Log</text>
  <rect x="120" y="250" width="710" height="80" rx="12" fill="#EDE7DA" stroke="#E4DCCB" stroke-width="2"/>
  <text x="475" y="285" text-anchor="middle" font-size="23">🔒 Original-Dokumente — werden nie verändert</text>
  <text x="475" y="315" text-anchor="middle" font-size="19" fill="#5C6670">Protokolle, Handbücher, Berichte — die Quelle der Wahrheit</text>
  <path d="M 80 290 C 30 290 30 175 112 175" stroke="#14466B" stroke-width="3" fill="none"/>
  <polygon points="110,167 126,175 110,183" fill="#14466B"/>
  <text x="46" y="230" text-anchor="middle" font-size="30">🤖</text>
</svg>

> „Eine KI wird nicht müde und vergisst keine Querverweise.
> **Die Pflege kostet fast nichts mehr.**“ — Andrej Karpathy (sinngemäß)

---

## So arbeitet das Wiki: drei Handgriffe

<svg class="diagram" width="1050" viewBox="0 0 1050 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="320" height="240" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="180" y="95" text-anchor="middle" font-size="48">📥</text>
  <text x="180" y="145" text-anchor="middle" font-size="25" font-weight="bold" fill="#14466B">Einsortieren</text>
  <text x="180" y="185" text-anchor="middle" font-size="19" fill="#5C6670">Neues Dokument einarbeiten,</text>
  <text x="180" y="212" text-anchor="middle" font-size="19" fill="#5C6670">verlinken, Widersprüche klären</text>
  <rect x="365" y="30" width="320" height="240" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="525" y="95" text-anchor="middle" font-size="48">💬</text>
  <text x="525" y="145" text-anchor="middle" font-size="25" font-weight="bold" fill="#14466B">Antworten</text>
  <text x="525" y="185" text-anchor="middle" font-size="19" fill="#5C6670">Im Wiki nachschlagen —</text>
  <text x="525" y="212" text-anchor="middle" font-size="19" fill="#5C6670">gute Erkenntnisse bleiben drin</text>
  <rect x="710" y="30" width="320" height="240" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="870" y="95" text-anchor="middle" font-size="48">🧹</text>
  <text x="870" y="145" text-anchor="middle" font-size="25" font-weight="bold" fill="#14466B">Aufräumen</text>
  <text x="870" y="185" text-anchor="middle" font-size="19" fill="#5C6670">Regelmäßig prüfen: Passt alles</text>
  <text x="870" y="212" text-anchor="middle" font-size="19" fill="#5C6670">noch zusammen? Fehlt ein Link?</text>
</svg>

Der Kern: Wissen wird **einmal eingearbeitet** — nicht bei jeder Frage neu gesucht.

---

## Das Ganze ist ein offener Standard

Google hat das Muster veröffentlicht: **Open Knowledge Format (OKF)**.

```
wiki/
├── index.md          ← die Startseite: Wegweiser für die KI
├── log.md            ← was wurde wann geändert?
├── kunden/…          ← eine Seite pro Kunde
├── systeme/…         ← eine Seite pro System
└── entscheidungen/…  ← eine Seite pro Entscheidung
```

- **Nur Textdateien** (Markdown) — jeder kann sie lesen, auch ohne KI
- Passt in **Git** — versioniert, teilbar, kein Spezial-System nötig
- **Format statt Plattform** — kein Anbieter-Lock-in

---

## So sieht eine Wiki-Seite aus

<div class="cols">
<div>

```markdown
---
type: Kunde
title: Helios Energie GmbH
tags: [kunden, enterprise]
---

# Helios Energie GmbH

Größter Kunde (~9.000 Anlagen).
**Gekündigt zum 30.09.2026.** Gründe:

1. [Störung im März](/vorfaelle/2026-03-14.md)
2. Fehlender CSV-Export
   → siehe [Roadmap](/produkt/roadmap-2026.md)
```

</div>
<div>

**① Steckbrief** — der Block zwischen den
`---`: Was für eine Seite ist das? Typ,
Titel, Schlagworte. So kann die KI (und
jedes Programm) Seiten gezielt finden.

**② Inhalt** — normaler Text: das von der
KI zusammengetragene, aktuelle Wissen.

**③ Links** — Querverweise: Sie verbinden
die Seiten zu einem Wissensnetz. Die KI
startet bei `index.md` und folgt ihnen
beim Antworten.

</div>
</div>

<small>Das Beispiel ist die Seite `kunden/helios-energie.md` aus unserer Demo —
genau die Seite, die gleich in Runde 2 die vollständige Antwort liefert.</small>

---

## Der Unterschied in einem Satz

<svg class="diagram" width="1000" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="20" width="430" height="160" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="255" y="78" text-anchor="middle" font-size="42">🔍</text>
  <text x="255" y="140" text-anchor="middle" font-size="26" font-weight="bold" fill="#14466B">RAG findet Textstellen.</text>
  <rect x="530" y="20" width="430" height="160" rx="16" fill="#FFFFFF" stroke="#B4551D" stroke-width="3"/>
  <text x="745" y="78" text-anchor="middle" font-size="42">📚</text>
  <text x="745" y="122" text-anchor="middle" font-size="26" font-weight="bold" fill="#B4551D">Das Wiki kennt</text>
  <text x="745" y="156" text-anchor="middle" font-size="26" font-weight="bold" fill="#B4551D">die Zusammenhänge.</text>
</svg>

| | 🔍 RAG | 📚 LLM-Wiki |
|---|---|---|
| Neues Dokument | wird nur abgelegt | wird eingearbeitet |
| Widersprüche | bleiben drin | werden geklärt |
| Erkenntnisse | gehen verloren | bleiben im Wiki |

---

## Zusammengefasst: die Vorteile des LLM-Wikis

<svg class="diagram" width="1000" viewBox="0 0 1050 420" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="180" y="75" text-anchor="middle" font-size="38">📖</text>
  <text x="180" y="125" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Die ganze Geschichte</text>
  <text x="180" y="158" text-anchor="middle" font-size="17" fill="#5C6670">verbindet Wissen aus vielen Dokumenten</text>
  <rect x="365" y="20" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="525" y="75" text-anchor="middle" font-size="38">⚖️</text>
  <text x="525" y="125" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Widersprüche geklärt</text>
  <text x="525" y="158" text-anchor="middle" font-size="17" fill="#5C6670">es gilt immer der aktuelle Stand</text>
  <rect x="710" y="20" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="870" y="75" text-anchor="middle" font-size="38">🌱</text>
  <text x="870" y="125" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Wissen wächst</text>
  <text x="870" y="158" text-anchor="middle" font-size="17" fill="#5C6670">gute Antworten bleiben erhalten</text>
  <rect x="20" y="220" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="180" y="275" text-anchor="middle" font-size="38">🧭</text>
  <text x="180" y="325" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Nachvollziehbar</text>
  <text x="180" y="358" text-anchor="middle" font-size="17" fill="#5C6670">Quellenangaben + Änderungs-Log</text>
  <rect x="365" y="220" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="525" y="275" text-anchor="middle" font-size="38">👀</text>
  <text x="525" y="325" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Für Menschen lesbar</text>
  <text x="525" y="358" text-anchor="middle" font-size="17" fill="#5C6670">nützlich auch ganz ohne KI</text>
  <rect x="710" y="220" width="320" height="180" rx="16" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="870" y="275" text-anchor="middle" font-size="38">🔓</text>
  <text x="870" y="325" text-anchor="middle" font-size="22" font-weight="bold" fill="#14466B">Offener Standard</text>
  <text x="870" y="358" text-anchor="middle" font-size="17" fill="#5C6670">nur Textdateien — kein Lock-in</text>
</svg>

**RAG** bleibt gut fürs schnelle Nachschlagen — das **Wiki** gewinnt, sobald
Wissen zusammenhängt und lebt.

---

## Gleich live: 5 Runden, gleiche Fragen, beide Systeme

<svg class="diagram" width="1050" viewBox="0 0 1050 250" xmlns="http://www.w3.org/2000/svg">
  <path d="M 105 90 H 945" stroke="#E4DCCB" stroke-width="4"/>
  <circle cx="105" cy="90" r="38" fill="#14466B"/>
  <text x="105" y="102" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="bold">1</text>
  <text x="105" y="165" text-anchor="middle" font-size="20" font-weight="bold">Warm werden</text>
  <text x="105" y="192" text-anchor="middle" font-size="17" fill="#5C6670">beide gut ✅</text>
  <circle cx="315" cy="90" r="38" fill="#14466B"/>
  <text x="315" y="102" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="bold">2</text>
  <text x="315" y="165" text-anchor="middle" font-size="20" font-weight="bold">Die ganze Geschichte</text>
  <text x="315" y="192" text-anchor="middle" font-size="17" fill="#5C6670">RAG bleibt lückenhaft</text>
  <circle cx="525" cy="90" r="38" fill="#14466B"/>
  <text x="525" y="102" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="bold">3</text>
  <text x="525" y="165" text-anchor="middle" font-size="20" font-weight="bold">Der Widerspruch</text>
  <text x="525" y="192" text-anchor="middle" font-size="17" fill="#5C6670">100 oder 500?</text>
  <circle cx="735" cy="90" r="38" fill="#B4551D"/>
  <text x="735" y="102" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="bold">4</text>
  <text x="735" y="165" text-anchor="middle" font-size="20" font-weight="bold">Live dazulernen</text>
  <text x="735" y="192" text-anchor="middle" font-size="17" fill="#5C6670">dem Wiki zusehen 👀</text>
  <circle cx="945" cy="90" r="38" fill="#14466B"/>
  <text x="945" y="102" text-anchor="middle" font-size="30" fill="#FFFFFF" font-weight="bold">5</text>
  <text x="945" y="165" text-anchor="middle" font-size="20" font-weight="bold">Wissen bleibt</text>
  <text x="945" y="192" text-anchor="middle" font-size="17" fill="#5C6670">Antwort wird Wiki-Seite</text>
</svg>

Unsere Spielwiese: die erfundene Firma **SolarFlow** mit 14 echten* Dokumenten.
<small>*echt aussehend — Protokolle, Handbücher, ein Störungsbericht und eine Kündigung.</small>

---

## Blick unter die Haube: so ist die Demo gebaut

<svg class="diagram" width="1030" viewBox="0 0 1030 430" xmlns="http://www.w3.org/2000/svg">
  <text x="20" y="38" font-size="21" fill="#5C6670" font-weight="bold">Daten hinein — pro Dokument einmal:</text>
  <rect x="20" y="58" width="230" height="120" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="135" y="105" text-anchor="middle" font-size="22">📄 Dokumente</text>
  <text x="135" y="135" text-anchor="middle" font-size="17" fill="#5C6670">Ordner corpus/</text>
  <path d="M 260 90 H 350" stroke="#14466B" stroke-width="3"/><polygon points="350,82 366,90 350,98" fill="#14466B"/>
  <rect x="376" y="58" width="300" height="64" rx="12" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="526" y="86" text-anchor="middle" font-size="18">✂️ zerschneiden + Zahlencode</text>
  <text x="526" y="110" text-anchor="middle" font-size="15" fill="#5C6670">(Embeddings — lokal, gratis)</text>
  <path d="M 686 90 H 756" stroke="#14466B" stroke-width="3"/><polygon points="756,82 772,90 756,98" fill="#14466B"/>
  <rect x="782" y="58" width="228" height="64" rx="12" fill="#FFFFFF" stroke="#14466B" stroke-width="2"/>
  <text x="896" y="97" text-anchor="middle" font-size="18" fill="#14466B" font-weight="bold">🗄️ Vektor-Datenbank</text>
  <path d="M 260 146 H 350" stroke="#B4551D" stroke-width="3"/><polygon points="350,138 366,146 350,154" fill="#B4551D"/>
  <rect x="376" y="130" width="300" height="64" rx="12" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="526" y="158" text-anchor="middle" font-size="18">🤖 Ingest-Agent liest, verknüpft,</text>
  <text x="526" y="182" text-anchor="middle" font-size="18">klärt Widersprüche, führt Log</text>
  <path d="M 686 162 H 756" stroke="#B4551D" stroke-width="3"/><polygon points="756,154 772,162 756,170" fill="#B4551D"/>
  <rect x="782" y="130" width="228" height="64" rx="12" fill="#FFFFFF" stroke="#B4551D" stroke-width="2"/>
  <text x="896" y="169" text-anchor="middle" font-size="18" fill="#B4551D" font-weight="bold">📚 Wiki (Markdown)</text>
  <text x="20" y="252" font-size="21" fill="#5C6670" font-weight="bold">Fragen beantworten — im Browser (Streamlit):</text>
  <rect x="20" y="272" width="230" height="120" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="135" y="320" text-anchor="middle" font-size="22">❓ Frage</text>
  <text x="135" y="350" text-anchor="middle" font-size="17" fill="#5C6670">läuft an beide Systeme</text>
  <path d="M 260 305 H 350" stroke="#14466B" stroke-width="3"/><polygon points="350,297 366,305 350,313" fill="#14466B"/>
  <rect x="376" y="272" width="300" height="64" rx="12" fill="#F6F2E9" stroke="#E4DCCB" stroke-width="2"/>
  <text x="526" y="300" text-anchor="middle" font-size="18">🔍 RAG: 4 passende Schnipsel</text>
  <text x="526" y="324" text-anchor="middle" font-size="18">📚 Wiki: Agent liest Seiten</text>
  <path d="M 686 305 H 756" stroke="#14466B" stroke-width="3"/><polygon points="756,297 772,305 756,313" fill="#14466B"/>
  <rect x="782" y="272" width="228" height="120" rx="14" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="2"/>
  <text x="896" y="315" text-anchor="middle" font-size="20">☁️ ein KI-Modell</text>
  <text x="896" y="345" text-anchor="middle" font-size="16" fill="#5C6670">für beide Seiten —</text>
  <text x="896" y="368" text-anchor="middle" font-size="16" fill="#5C6670">fairer Vergleich</text>
</svg>

<small>Wenige hundert Zeilen Python. Neues Dokument einspeisen = ein Klick in
der App (oder `make ingest`) — beide Wege werden gleichzeitig gefüttert.</small>

---

# Demo 🎬

```bash
make reset && make run
```

---

## Zum Weiterlesen

- Andrej Karpathy — die LLM-Wiki-Idee:
  `gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
- Google Cloud — das Open Knowledge Format:
  `cloud.google.com/blog/products/data-analytics/…`
- Dieses Projekt: alles zum Selbst-Ausprobieren — `make reset` genügt.

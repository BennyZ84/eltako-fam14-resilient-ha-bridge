# Robuste Eltako-FAM14-Anbindung für Home Assistant

Dieses Repository beschreibt eine praxiserprobte Architektur, um einen **Eltako-FAM14-/Baureihe-14-RS485-Bus** mit **Home Assistant** zu verbinden. Der normale Steuerweg läuft über einen **ESP32 als TCP↔RS485-Gateway**; ein **EnOcean USB300** bildet einen unabhängigen Funk-Notpfad.

Die Public-Version ist bewusst anonymisiert. Private IP-Adressen, echte Sender-IDs, Zugangsdaten, die konkrete ESP32-Pinbelegung und der individuelle Bridge-Quellcode gehören nicht in ein öffentliches Repository.

## Architektur

```text
Normalbetrieb:
Home Assistant → MQTT → Linux-Bridge → TCP → ESP32 → RS485 → FAM14

FTR/Sensoren:
EnOcean-Funksensor → USB300 → EnOcean MQTT → Home Assistant

Failover:
Home Assistant → MQTT → EnOcean MQTT → USB300 → EnOcean-Funk → FAM14-Aktor
```

Der USB300 wird **nicht** als zweiter dauernd konkurrierender Sender benutzt. Er übernimmt nur, wenn der Primärweg als ausgefallen erkannt wird oder eine echte Bestätigung innerhalb des konfigurierten Zeitfensters ausbleibt.

## Enthalten

- Wiederaufbau von null
- ESP32-/LXC-/MQTT-Architektur
- USB300-Base-ID und Senderbereich
- A5-38-08-Schalttelegramme
- A5-3F-7F-Rollladen-Telegramme
- FTR/F4HK-Zuordnung und beobachtete Temperaturdekodierung
- ACK/Pending-basierter Failover
- ESP32-Totalausfall-Notbetrieb
- Diagnose und Disaster Recovery
- Generator für `enoceanmqtt.devices` aus einer CSV-Geräteliste

Starte mit [`docs/setup.md`](docs/setup.md) und [`docs/architecture.md`](docs/architecture.md).

## Quellen, Inspiration und ähnliche Projekte

Die Public-Version nennt ausdrücklich die Projekte, die als technische Quelle, Upstream-Referenz oder Dokumentations-Inspiration geholfen haben:

- [`grimmpp/home-assistant-eltako`](https://github.com/grimmpp/home-assistant-eltako) — direkte technische Referenz/Vergleich für Baureihe 14, FAM14/USB300, EEPs und Climate.
- [`grimmpp/eltako14bus`](https://github.com/grimmpp/eltako14bus) — direkte RS485-/Baureihe-14-Protokollreferenz.
- [`embyt/enocean-mqtt`](https://github.com/embyt/enocean-mqtt) — operative Referenz für USB300 ↔ MQTT und Senden mit Sender-IDs.
- [`kipe/enocean`](https://github.com/kipe/enocean) — Upstream-Referenz für EnOcean/ESP3.
- [`cvanlabe/Eltako-home-automation`](https://github.com/cvanlabe/Eltako-home-automation) — praktische Dokumentations- und Inbetriebnahme-Inspiration.

Ausführlich mit Community- und Herstellerquellen: [`SOURCES.md`](SOURCES.md). Es wurde **kein Fremdcode kopiert**.

Unser Schwerpunkt ist die **Kombination aus kabelgebundenem Primärweg und unabhängigem Funk-Failover** mit echter Bestätigungslogik.

## Lizenz

MIT für die hier neu erstellten Inhalte. Verlinkte Abhängigkeiten und Projekte behalten ihre eigenen Lizenzen.

# Related open-source projects

Research date: **2026-08-13**.

For the full attribution list, including upstream libraries, vendor documentation and community references, see [`../SOURCES.md`](../SOURCES.md).

## home-assistant-eltako

Repository: <https://github.com/grimmpp/home-assistant-eltako>

A mature Home Assistant custom integration for Eltako Series 14 / EnOcean devices. It supports Eltako FAM14/FGW14-USB, EnOcean USB300 and multiple actuator/sensor EEPs, including switching, covers and experimental climate support.

**Role for this project:** direct technical reference and comparison point. Its documentation and supported-EEP lists helped validate terminology and protocol assumptions. No source code is copied here.

**Overlap with this repository:** Eltako devices, FAM14, EnOcean profiles, Home Assistant, USB300.

**Different focus here:** an external MQTT bridge with ESP32 TCP↔RS485 as primary control plus USB300 as a separate acknowledgement-aware failover path.

## eltako14bus

Repository: <https://github.com/grimmpp/eltako14bus>

Python library and tooling for interacting with the Eltako Series 14 RS485 bus, including raw bus operations and memory inspection.

**Role for this project:** direct Series 14 protocol/reference material used to cross-check behavior observed on a real bus. No library source code is bundled here.

## enocean-mqtt

Repository: <https://github.com/embyt/enocean-mqtt>

Receives EnOcean serial data and publishes it to MQTT. It also supports outbound telegram construction and sender IDs within the USB transceiver Base-ID range.

**Role for this project:** operational dependency/reference for the USB300↔MQTT path. The public device-file and MQTT request examples in this repository are designed to interoperate with its documented configuration model.

**Different focus here:** this repository defines how to use that ability as an inactive-by-default backup for an independent wired FAM14 primary path.

## Python EnOcean

Repository: <https://github.com/kipe/enocean>

Python library for reading and controlling EnOcean devices over the serial protocol.

**Role for this project:** upstream EnOcean/ESP3 technical reference. It is part of the ecosystem beneath USB300 tooling; no source code is copied here.

## Eltako-home-automation

Repository: <https://github.com/cvanlabe/Eltako-home-automation>

A practical, installation-oriented walkthrough of Eltako hardware, PCT14 programming and Home Assistant integration.

**Role for this project:** documentation/commissioning inspiration. Its focus on retaining physical-control reliability and documenting a recoverable installation is closely aligned with this project's goals. The architecture here was developed independently.

## Home Assistant community thread

Eltako “Baureihe 14 – RS485” (EnOcean) Debugging:
<https://community.home-assistant.io/t/eltako-baureihe-14-rs485-enocean-debugging/49712>

**Role for this project:** useful historical and troubleshooting context, including community experiments around F4HK/A5-10-06 and gateway behavior. Community observations are not treated as normative specifications.

## Vendor documentation

Eltako's current radio-telegram/teach-in documentation should be treated as a primary product reference:
<https://www.eltako.com/de/download_file/technische-daten-der-funk-aktoren-einlernliste-reichweiten-und-inhalte-der-eltako-funktelegramme/>

For EnOcean EEP definitions, use the current EnOcean Alliance specifications:
<https://www.enocean-alliance.org/specifications/>

## Why this repository is separate

The goal is not to duplicate the functionality of the projects above. It is to document and package an operational pattern that combines:

- a networked RS485 primary path,
- independent EnOcean RF reception,
- independent USB300 RF transmission,
- real acknowledgement/pending tracking,
- automatic timeout/offline failover,
- a direct emergency control UI,
- disaster-recovery mappings.

No third-party source code is copied into this repository.

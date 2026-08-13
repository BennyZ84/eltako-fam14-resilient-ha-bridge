# Sources, upstream projects, and inspiration

Research/verification date: **2026-08-13**.

This repository is an independent reference architecture. It would not be useful without the public work that documents and implements important parts of the Eltako Series 14 and EnOcean ecosystem. The projects below are credited according to the role they played.

## Direct technical references

### grimmpp/home-assistant-eltako

<https://github.com/grimmpp/home-assistant-eltako>

**Role:** direct technical reference and comparison point.

The project provides a mature Home Assistant integration for Eltako Series 14 / EnOcean systems and documents supported gateways and EEPs, including FAM14/FGW14-USB, USB300, A5-38-08 switching, 3F-7F cover control, and experimental A5-10-06 climate support.

It was especially useful as a reference for:

- Series 14 device/profile terminology,
- supported EnOcean equipment profiles,
- FAM14/USB300 gateway concepts,
- heating/cooling behavior and climate implementation context,
- links to the broader Eltako/Home Assistant ecosystem.

No source code from this project is copied into this repository.

### grimmpp/eltako14bus

<https://github.com/grimmpp/eltako14bus>

**Role:** direct Series 14 RS485/protocol reference.

This Python library implements participation in and control of the Eltako Series 14 RS485 bus and includes tools for raw bus interaction and device-memory inspection. It is a key public reference for understanding the Series 14 bus model and for validating assumptions made while diagnosing a real installation.

No source code from this project is copied into this repository.

### embyt/enocean-mqtt

<https://github.com/embyt/enocean-mqtt>

**Role:** operational dependency/reference for the USB300↔MQTT path.

The public examples in this repository intentionally target concepts exposed by `enocean-mqtt`, including configured sender IDs, `ignore = 1`, MQTT `/req/...` field updates, and explicit send requests. Its documented ability to transmit with sender IDs inside the transceiver Base-ID range is fundamental to the USB300 fallback design.

No `enocean-mqtt` source code is bundled here. The projects remain separately licensed.

### kipe/enocean

<https://github.com/kipe/enocean>

**Role:** upstream EnOcean/ESP3 reference.

The Python EnOcean library provides the serial-protocol foundation used by projects in this ecosystem, including USB300 communication. It is cited here as an upstream technical reference for EnOcean packet handling and transceiver behavior.

No source code from this project is copied into this repository.

## Documentation inspiration and community context

### cvanlabe/Eltako-home-automation

<https://github.com/cvanlabe/Eltako-home-automation>

**Role:** documentation and commissioning inspiration.

This project documents a practical journey from physical Eltako installation and PCT14 programming to Home Assistant integration. Its emphasis on preserving local wall-switch operation, avoiding a fragile single point of failure, documenting teach-in steps, and making installations recoverable is strongly aligned with the operational goals of this repository.

The architecture and helper code here were developed independently; this is a credit for useful documentation and practical context, not a statement that code was copied.

### Home Assistant Community — Eltako “Baureihe 14 – RS485” (EnOcean) Debugging

<https://community.home-assistant.io/t/eltako-baureihe-14-rs485-enocean-debugging/49712>

**Role:** community troubleshooting and historical implementation context.

The long-running community thread contains practical reports about FAM14/FGW14 behavior, sender IDs, A5-10-06/F4HK experiments, gateway configuration, and migration pitfalls. It is useful supporting context when a real installation behaves differently from a simplified protocol model.

Community posts are treated as observations, not normative specifications.

## Vendor and specification references

### Eltako downloads — radio telegram contents / teach-in information

<https://www.eltako.com/de/download_file/technische-daten-der-funk-aktoren-einlernliste-reichweiten-und-inhalte-der-eltako-funktelegramme/>

**Role:** vendor documentation reference.

Use the current Eltako documents to verify teach-in settings, supported sensors/actuators, telegram content, and product-specific behavior before transmitting to production equipment.

### EnOcean Alliance specifications

<https://www.enocean-alliance.org/specifications/>

**Role:** protocol/EEP specification reference.

Use the current EnOcean Alliance documentation for normative EnOcean Equipment Profile definitions and serial/radio protocol semantics where applicable.

## What is original in this repository

The following are presented here as independently assembled operational patterns and field observations:

- the two-path architecture with ESP32 TCP↔RS485 as the normal path and USB300 RF as an independent fallback;
- acknowledgement/pending-aware fallback rather than always-on duplicate transmission;
- an ESP32-outage emergency-control path that calls the USB300 dispatcher directly;
- the recovery-oriented mapping/generation workflow;
- the field-verified F4HK feedback mapping and temperature-byte observations documented in `docs/climate-f4hk.md`;
- the example generator, tests, sanitizer, and repository documentation structure.

Where a behavior is based on a real installation rather than a normative vendor specification, the documentation labels it as a **field observation** and asks readers to verify it on their own hardware.

## Licensing note

This repository does not vendor or redistribute source code from the projects listed above. Links, names, and factual interoperability references do not change the license of the original material in this repository. If you later copy or adapt third-party code, review that project's current license and preserve all required notices before publishing.

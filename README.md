# Resilient Eltako FAM14 bridge for Home Assistant

[Deutsche Version](README.de.md)

A field-tested reference architecture for integrating an **Eltako Series 14 / FAM14 RS485 bus** with **Home Assistant**, using an **ESP32 TCP↔RS485 gateway** as the primary path and an **EnOcean USB300** as an independent RF fallback.

> **Status:** reference implementation / documentation project. This is not an official Eltako or Home Assistant project.

## Why this exists

Existing open-source projects already cover important pieces of the puzzle. This work explicitly builds on their public knowledge and gives credit according to how each source was used:

- [`grimmpp/home-assistant-eltako`](https://github.com/grimmpp/home-assistant-eltako) — direct technical reference/comparison for Eltako Series 14, FAM14/USB300, EEPs and climate support.
- [`grimmpp/eltako14bus`](https://github.com/grimmpp/eltako14bus) — direct Series 14 RS485/protocol reference.
- [`embyt/enocean-mqtt`](https://github.com/embyt/enocean-mqtt) — operational dependency/reference for USB300↔MQTT and outbound sender-ID handling.
- [`kipe/enocean`](https://github.com/kipe/enocean) — upstream EnOcean serial/ESP3 reference.
- [`cvanlabe/Eltako-home-automation`](https://github.com/cvanlabe/Eltako-home-automation) — practical documentation and commissioning inspiration.

See [`SOURCES.md`](SOURCES.md) for detailed attribution, community references, vendor/specification links, and a clear statement of what is original here. No third-party source code is copied into this repository.

This repository documents a different operational design:

```text
PRIMARY PATH
Home Assistant
   │ MQTT
   ▼
Linux bridge service
   │ TCP
   ▼
ESP32 TCP ↔ RS485 gateway
   │ RS485
   ▼
Eltako FAM14 / Series 14 bus

RF TELEMETRY
Room controller / EnOcean sensor
   │ 868 MHz
   ▼
USB300 → EnOcean-MQTT → Home Assistant

FAILOVER PATH
Home Assistant
   │ MQTT
   ▼
EnOcean-MQTT → USB300
   │ 868 MHz
   ▼
Eltako actuator
```

The key idea is **single-writer primary control over RS485**, plus a **physically independent RF backup path** that only transmits when the primary path is confirmed unavailable or a command is not acknowledged within a configurable timeout.

## Highlights

- ESP32 used as a network-transparent TCP↔RS485 gateway.
- Linux/Python bridge as the single normal sender to the FAM14 bus.
- MQTT as the Home Assistant-facing API and discovery/state transport.
- EnOcean USB300 used for sensor reception and actuator fallback transmission.
- Pending/acknowledgement-aware failover instead of blind duplicate sends.
- Immediate fallback when bridge heartbeat/status is down.
- Manual emergency dashboard can work even if the ESP32 is completely dead.
- F4HK/FHK temperature feedback decoding documented from real bus observations.
- Explicit warning that cooling/heating mode broadcast control must be learned and verified per installation.
- Disaster-recovery checklist designed to rebuild the installation from zero.

## Repository layout

```text
docs/
  architecture.md       System design and safety model
  setup.md              Build from zero
  usb300-failover.md    RF backup design and telegram examples
  climate-f4hk.md       FTR/F4HK notes and decoded feedback
  home-assistant.md     MQTT entities, dispatcher and failover logic
  troubleshooting.md    Symptom-based diagnostics
  recovery.md           Disaster recovery procedure
  related-projects.md   Existing projects and how this differs
SOURCES.md               Sources, upstream projects and inspiration
examples/
  device-map.example.csv
  enoceanmqtt.devices.example
  bridge-config.example.yaml
  home-assistant/
    fam14_usb300_failover.example.yaml
tools/
  generate_usb300_devices.py
  sanitize_check.py
tests/
  test_generate_usb300_devices.py
```

## Quick start

1. Read [`docs/architecture.md`](docs/architecture.md) before connecting anything to the FAM14 bus.
2. Inventory the actuator bus addresses, learned sender IDs, EEPs and cover timing data.
3. Build or restore the ESP32 TCP↔RS485 gateway.
4. Run one bridge process only and verify bidirectional bus feedback.
5. Add MQTT discovery/state publication.
6. Configure USB300 reception and **read its Base ID before changing it**.
7. Add RF backup senders only for sender IDs the actuators are already trained to accept.
8. Enable automatic fallback only after primary acknowledgements and direct USB300 transmissions are independently verified.

Full procedure: [`docs/setup.md`](docs/setup.md).

## Important safety rules

- **Do not run two independent RS485 writers** against the same FAM14 gateway.
- **Do not guess EnOcean sender IDs or EEPs.** Learn or observe them first.
- **Do not repeatedly rewrite a USB300/TCM310 Base ID.** It is persistent and write-cycle limited.
- **Do not treat TCP-connectivity alone as a successful actuator command.** Require real bus acknowledgement/state feedback where possible.
- **Do not blindly transmit a global heating/cooling mode telegram.** Verify which F4HK/FHK devices have learned that sender/function.
- Prefer state-preserving tests: send OFF to an already-off relay, STOP to a stationary shutter, or re-send the current thermostat target.

## What is intentionally not included

This public repository does **not** contain:

- private IP addresses from a real home,
- real household sender IDs,
- MQTT credentials,
- SSH credentials or keys,
- a site-specific ESP32 pinout,
- a site-specific bridge source file.

Those values belong in your private deployment repository or secrets manager. Example values here use documentation placeholders.

## Tested concepts

The architecture has been validated on a real Eltako Series 14 installation with lighting, relays, covers, F4HK channels and EnOcean room controllers. Observed protocol details are documented as **field observations**, not as a substitute for Eltako or EnOcean specifications.

## Sources, credits and related projects

See [`SOURCES.md`](SOURCES.md) for explicit attribution and [`docs/related-projects.md`](docs/related-projects.md) for the architectural comparison. This project is complementary to, not a replacement for, the established Eltako and EnOcean libraries/integrations.

## Support the project

If this project helps you, you can [support further hardware testing via PayPal](https://paypal.me/BenjaminZapf492). Contributions are used to purchase additional Eltako and EnOcean components for reproducible tests and documentation.

## License

MIT for the original material in this repository. Dependencies and linked projects retain their own licenses. No third-party source code is bundled here.

## Disclaimer

Working on an electrical/building automation bus can operate real loads, shutters and HVAC equipment. Validate telegrams on a safe test channel before production use. You are responsible for the electrical and functional safety of your installation.

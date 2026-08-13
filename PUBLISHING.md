# Publishing checklist

Suggested repository name:

`eltako-fam14-resilient-ha-bridge`

Suggested GitHub description:

> Resilient Eltako FAM14/Home Assistant reference architecture: ESP32 TCP-RS485 primary bridge with MQTT, USB300 EnOcean RF failover, F4HK climate notes and disaster recovery.

Suggested topics:

`home-assistant`, `eltako`, `fam14`, `enocean`, `usb300`, `esp32`, `rs485`, `mqtt`, `home-automation`, `failover`

## Before first push

```bash
python -m unittest discover tests -v
python tools/sanitize_check.py
python tools/generate_usb300_devices.py examples/device-map.example.csv > /tmp/generated.devices
```

Then manually check:

- [ ] no real MQTT/SSH/GitHub credentials
- [ ] no private deployment IP/DNS names unless intentionally public
- [ ] no real household sender IDs unless intentionally public
- [ ] no PCT14 export with private mappings
- [ ] example data clearly marked as example
- [ ] LICENSE and NOTICE are present
- [ ] linked third-party projects are credited without copying their source

## Initial Git commands

```bash
git init
git add .
git commit -m "Initial public release"
git branch -M main
# Add the remote created in GitHub, then:
git push -u origin main
```

## Recommended first release

Tag the first reviewed version only after the repository is visible and links render correctly:

```bash
git tag -a v0.1.0 -m "Initial documentation release"
git push origin v0.1.0
```

## Public/private split

Keep a separate private deployment repository (or secrets storage) containing:

- actual ESP32/LXC addresses,
- actual USB300 Base ID,
- actual sender/bus mappings,
- ESP32 firmware/pinout,
- production bridge source/config,
- PCT14 backups.

Do not merge that private data back into this public reference repository.

- [ ] Review `SOURCES.md` before every public release and add newly used sources/inspirations.

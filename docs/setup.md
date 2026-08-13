# Setup from zero

This chapter is intentionally deployment-oriented. Replace all example addresses and IDs with values from your installation.

## 1. Inventory the existing Eltako installation

Before changing anything, record:

- FAM14 bus addresses,
- actuator type per bus address,
- learned sender IDs,
- EEP/profile used for each sender,
- F4HK base/channel mapping,
- cover direction/timing information,
- physical EnOcean room-controller IDs,
- existing PCT14 configuration/export if available.

Back up PCT14 data before re-teaching devices.

## 2. Build the ESP32 TCP↔RS485 gateway

Requirements:

- ESP32 with stable power,
- suitable RS485 transceiver,
- correct A/B wiring to the FAM14 bus,
- firmware providing a bidirectional TCP socket,
- static/reserved LAN address.

Example deployment variables:

```text
ESP32_HOST=192.0.2.20
ESP32_PORT=6638
```

`192.0.2.0/24` is a documentation network and should be replaced.

Verify:

1. TCP port is reachable.
2. Data can travel in both directions.
3. A real FAM14 actuator feedback telegram is observed.

A successful TCP connect does not prove RS485 functionality.

## 3. Create the Linux bridge host

A small Debian/Ubuntu VM/LXC is sufficient.

Suggested layout:

```text
/opt/fam14-bridge/
  bridge.py
  config.yaml
  .venv/
```

Run the bridge as a dedicated systemd service. Use a pinned dependency file (`requirements.txt` or lock file) and keep it in version control.

Example systemd skeleton:

```ini
[Unit]
Description=FAM14 MQTT Bridge
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/fam14-bridge
ExecStart=/opt/fam14-bridge/.venv/bin/python /opt/fam14-bridge/bridge.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Use your real unit file as the recovery source; this is only a skeleton.

## 4. Implement MQTT command/state transport

Minimum command topic:

```text
fam14/cmd
```

Recommended diagnostic/state concepts:

```text
fam14/bridge/status
fam14/bridge/heartbeat
fam14/state/<device>
fam14/pending/<device>
fam14/warn/<device>
```

Use retained state/discovery only where stale values cannot be confused with a fresh acknowledgement.

## 5. Verify primary control before adding failover

For every actuator class:

- send a state-preserving command,
- verify the exact outgoing FAM14 telegram,
- verify a real bus feedback telegram,
- verify pending returns to idle,
- verify warning clears.

Do not continue until the primary path is stable.

## 6. Install USB300 / EnOcean-MQTT

Use a stable serial path such as:

```text
/dev/serial/by-id/usb-EnOcean_GmbH_USB_300_<SERIAL>-if00-port0
```

Do not depend on `/dev/ttyUSB0` if other USB serial devices are present.

For the EnOcean-MQTT project/add-on, configure:

- serial path,
- MQTT broker,
- discovery prefix if required,
- device file,
- packet/debug logging during commissioning.

## 7. Read USB300 Base ID first

Read the TCM310 Base ID using ESP3 command `CO_RD_IDBASE` before writing anything.

A sender configured in EnOcean-MQTT must lie in the allowed Base-ID range, typically Base ID through Base ID + 127.

Only change the Base ID when there is a deliberate migration plan. Treat writes as scarce persistent hardware operations.

## 8. Create RF backup sender mappings

Populate [`examples/device-map.example.csv`](../examples/device-map.example.csv) with your learned sender offsets and run:

```bash
python tools/generate_usb300_devices.py \
  examples/device-map.example.csv \
  > enoceanmqtt.devices.generated
```

Review the generated file before copying it into production.

## 9. Test USB300 transmission independently

Use state-preserving commands:

- relay already OFF → send OFF,
- stationary cover → send STOP.

Verify in the USB300/EnOcean log that a radio packet was actually sent and accepted by the transceiver.

## 10. Enable failover

Only now enable the automatic fallback logic. Perform a normal primary-path test and prove that **no USB300 duplicate telegram** is sent after a successful acknowledgement.

Then test the offline path in a controlled maintenance window.

## 11. Build the emergency dashboard

Create buttons that call the RF dispatcher directly. Do not route those buttons through entities that depend on the failed bridge.

## 12. Climate / F4HK

Read [`climate-f4hk.md`](climate-f4hk.md) before enabling heating/cooling forwarding or mode broadcast.

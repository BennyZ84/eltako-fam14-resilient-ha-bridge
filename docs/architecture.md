# Architecture

## Design goals

1. Keep the FAM14 RS485 bus as the deterministic primary path.
2. Expose a simple MQTT API to Home Assistant.
3. Preserve real bus acknowledgements/state feedback.
4. Receive EnOcean room-controller telemetry independently through USB300.
5. Provide a second transmission path that does not depend on the ESP32.
6. Avoid duplicate sends during healthy operation.
7. Make every component replaceable without re-discovering all field mappings.

## Components

### FAM14 / Series 14 bus

The Eltako bus is the actuator layer. Typical installations contain FSR/FUD switching/dimming devices, FSB covers and FHK/F4HK heating/cooling actuators.

### ESP32 TCP↔RS485 gateway

The ESP32 should behave as a transparent bidirectional gateway:

```text
TCP socket <-> UART/RS485 transceiver <-> FAM14 bus
```

Use a stable IP address or DHCP reservation and a fixed TCP port. The exact UART pins, DE/RE wiring and firmware depend on the board and transceiver and **must be version-controlled privately**.

### Linux bridge service

The bridge owns the normal TCP connection to the ESP32 and is the **single normal writer** to the FAM14 bus. Its responsibilities can include:

- MQTT command subscription,
- serializing outgoing bus messages,
- parsing FAM14 feedback,
- publishing states/pending/ack/warnings,
- Home Assistant MQTT discovery,
- translating EnOcean room-controller values to learned F4HK senders,
- heating/cooling mode refresh.

A local watchdog may restart the bridge if the process or TCP link is genuinely broken. Avoid a second Home Assistant watchdog that fights the local watchdog.

### Home Assistant / MQTT

Recommended command API:

```text
fam14/cmd
```

Example payloads:

```text
hall_on
hall_off
cover_office_open
cover_office_stop
cover_office_close
```

For each commandable object expose enough diagnostics to tell the difference between:

- command accepted by HA,
- command forwarded to the bridge,
- command pending on the bus,
- real actuator/bus acknowledgement,
- timeout/warning.

### USB300 / EnOcean MQTT

USB300 is used in two roles:

1. receive physical EnOcean sensors/room controllers;
2. transmit backup commands using sender IDs already learned by the target actuators.

The backup path must remain operational when the ESP32 is unavailable.

## Failover state machine

A robust pattern is:

```text
on fam14/cmd:
  if command is unsupported by RF backup:
      do nothing extra
  else if bridge is offline OR heartbeat is stale/off:
      send command immediately over USB300
  else:
      snapshot the relevant pending object's last-change marker
      wait FAILOVER_TIMEOUT
      if pending is still non-idle OR pending never changed:
          send once over USB300
      else:
          primary path succeeded; do not RF-send
```

Why check **"pending never changed"** as well as **"pending stuck"**? A completely dead bridge may never create a pending cycle at all. A stale "online" heartbeat alone can otherwise delay detection.

The timeout must be chosen from measurements of your installation. In one field installation, the slowest successful primary acknowledgement was below 7 seconds, so 8 seconds provided a small margin. Do not copy that value blindly if your bus differs.

## Single-writer rule

Never run a diagnostic script that opens a second long-lived connection to the same RS485/TCP gateway while the production bridge is active. Multiple bus masters/readers can create timing problems, ambiguous feedback and misleading watchdog behavior.

## Manual emergency path

A Home Assistant emergency dashboard can call the USB300 dispatcher directly. It should not depend on the normal FAM14 entities because those may be unavailable when the ESP32 is down.

For covers, expose only OPEN / STOP / CLOSE unless you still have trustworthy independent position feedback. Percentage positioning is unsafe if the primary position model is unavailable.

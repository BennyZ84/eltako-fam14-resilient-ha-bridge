# USB300 RF failover

## Principle

The USB300 can transmit using sender IDs within its Base-ID window. If an Eltako actuator has already learned one of those IDs, USB300 can reproduce the corresponding EnOcean telegram independently of the ESP32/RS485 path.

This is powerful, but it must be configured deliberately to avoid competing controllers.

## Switch/relay profile observed in field use

For central-command style switching, **A5-38-08** was used successfully.

Observed data bytes:

```text
ON  = 01 00 00 09
OFF = 01 00 00 08
```

Example EnOcean-MQTT section:

```ini
[usb300_backup_example_relay]
address = 0xFFFFFFFF
rorg = 0xA5
func = 0x38
type = 0x08
sender = 0xFFAABB81
default_data = 0x01000008
ignore = 1
```

Example MQTT sequence:

```text
enoceanmqtt/usb300_backup_example_relay/req/COM  -> 1
enoceanmqtt/usb300_backup_example_relay/req/SW   -> 1 or 0
enoceanmqtt/usb300_backup_example_relay/req/send -> clear
```

`ignore = 1` is useful when the entry exists only as an outbound transmitter and should not create Home Assistant discovery clutter.

## Cover profile observed in field use

A5-3F-7F Universal was used as an outbound representation for learned Eltako cover commands.

Example device section:

```ini
[usb300_backup_cover_office]
address = 0xFFFFFFFF
rorg = 0xA5
func = 0x3F
type = 0x7F
sender = 0xFFAABBA1
ignore = 1
```

The working implementation supplied `raw_data` dynamically through MQTT rather than storing a colon-separated `raw_data` string in the device file.

Observed command shape:

```text
STOP  = 00:00:00:0A:80
OPEN  = <prefix-byte-1>:<prefix-byte-2>:01:0A:80
CLOSE = <prefix-byte-1>:<prefix-byte-2>:02:0A:80
```

The two-byte prefix is actuator/setup specific and must be learned from your installation; do not copy a random value.

Example MQTT sequence:

```text
enoceanmqtt/usb300_backup_cover_office/req/raw_data -> 00:F5:01:0A:80
enoceanmqtt/usb300_backup_cover_office/req/send     -> raw_data
```

## Why not keep both paths active all the time?

Two independent senders can create duplicate commands, confusing timing and difficult diagnostics. The intended model is:

- RS485 primary;
- USB300 silent during healthy operation;
- USB300 sends once after a proven failure/timeout.

## Base-ID migration

If the already-learned virtual sender IDs do not fit the current USB300 Base-ID range, choose one of these strategies:

1. Re-teach actuators to sender IDs inside the USB300 range.
2. Deliberately change the USB300 Base ID once, then read it back and document it.
3. Use a second EnOcean transmitter for a different sender-address range.

Do not dynamically switch Base IDs during normal operation.

## Failover timeout

Set the timeout from measured primary-path latency. Collect at least dozens of successful commands across device classes if possible and choose a margin above the worst normal response time.

A timeout that is too short creates duplicate radio traffic. A timeout that is too long weakens the failover benefit.


## References and provenance

The USB300/MQTT workflow in this chapter is designed around the public `embyt/enocean-mqtt` configuration/request model. `kipe/enocean` is cited as an upstream EnOcean serial/ESP3 reference. See [`../SOURCES.md`](../SOURCES.md).

The exact switch and cover command bytes shown above are documented as **field-verified examples** for one installation; verify them against your actuator teach-in, current Eltako documentation, and applicable EEP before production use.

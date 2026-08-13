# Home Assistant design

## Entity model

A simple architecture keeps all FAM14 entities under one MQTT bridge device while exposing user-facing lights, switches, covers and climate entities separately.

Recommended bridge diagnostics:

- status (`online`/`offline`),
- heartbeat,
- TCP link health,
- per-device pending state,
- per-device command-confirmed indicator,
- per-device warning text.

## RF dispatcher

Use one central Home Assistant script or external service to serialize all USB300 transmissions.

Recommended execution mode:

```text
queued
```

USB300 is a single serial transceiver. Even if multiple failover automations fire at once, the actual RF writes should be serialized.

## Automatic failover

The example package in [`examples/home-assistant/fam14_usb300_failover.example.yaml`](../examples/home-assistant/fam14_usb300_failover.example.yaml) demonstrates the pattern with documentation-only sample entities.

Important behavior:

1. Subscribe to the same command topic used by the primary bridge.
2. Ignore commands that have no RF backup mapping.
3. If bridge status/heartbeat is bad, call the RF dispatcher immediately.
4. Otherwise snapshot the pending object's last change, wait the timeout, and call RF only if:
   - pending is still not idle, or
   - pending never changed at all.

The second condition catches a dead bridge that stopped before creating a pending marker.

## No-double-send acceptance test

Before enabling production failover:

1. choose an already-off relay;
2. publish its OFF command through the primary path;
3. confirm the bus acknowledgement;
4. wait longer than `FAILOVER_TIMEOUT`;
5. verify the USB300 dispatcher did not run.

## Emergency dashboard

Create a separate view whose buttons invoke the RF dispatcher directly.

Do not call the ordinary FAM14 light/cover entities from this page; if those entities are unavailable, the emergency page would fail for the same reason as the normal path.

For covers, offer OPEN / STOP / CLOSE only unless independent position feedback survives the primary-gateway outage.

# Troubleshooting

## Bridge shows offline

1. Is the Linux bridge host reachable?
2. Is the bridge systemd service active?
3. Does its journal show connection/restart loops?
4. Is the ESP32 TCP port reachable?
5. Is there real bidirectional FAM14 traffic?
6. Is the local link watchdog restarting too aggressively?

## Bridge is online but actuator does not react

Check the per-device pending state and bus acknowledgement before manually using USB300. If automatic failover is enabled, let its timeout expire once instead of adding extra manual traffic.

## ESP32 is completely dead

The RF emergency path should still work for mapped relays/covers:

```text
Home Assistant -> MQTT -> EnOcean-MQTT -> USB300 -> RF -> actuator
```

If it does not, debug the USB300 path independently of the FAM14 bridge.

## USB300 receives nothing

- Verify the stable `/dev/serial/by-id/...` device exists.
- Verify the EnOcean-MQTT process is running.
- Check raw packet logging.
- Check recent `last_seen`/RSSI from known sensors.

## USB300 sends nothing

- Read the current Base ID.
- Verify the configured sender is inside the Base-ID window.
- Verify device-file EEP/function/type.
- Verify the MQTT request sequence.
- Look for a transceiver-level success/response packet in logs.

## EnOcean-MQTT fails after editing the device file

If a colon-separated cover `raw_data` was placed directly in a configuration field that expects an integer, remove it and set `raw_data` dynamically through MQTT at send time.

## Too many TCP clients to the ESP32

Look for:

- orphaned Python diagnostic processes,
- a second bridge instance,
- one-shot scripts that open a socket but never close it,
- overlapping health checks that create connections.

The primary bridge should normally own the persistent control connection.

## Unknown EnOcean senders

Classify before adding them:

- F4HK feedback family,
- FAM14 actuator feedback,
- your own USB300 transmit echo,
- genuinely unknown external sensor.

Use timestamp correlation with an already-known state change before assigning meaning to a telegram.

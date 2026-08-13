# Disaster recovery

## Back up these artifacts before you need them

1. Home Assistant full backup.
2. Linux bridge VM/LXC backup.
3. Bridge source code and pinned Python dependencies.
4. Bridge/watchdog systemd units.
5. ESP32 firmware/source and exact board/UART/RS485 pin mapping.
6. PCT14 project/export and actuator teach-in mapping.
7. EnOcean-MQTT configuration and device file.
8. USB300 Base ID and original/rollback Base ID if it was changed.
9. Device mapping CSV used to generate backup senders.
10. This repository plus a private deployment file containing real addresses.

## Home Assistant failure only

- Restore HA.
- Verify MQTT broker and EnOcean-MQTT.
- Do not rebuild ESP32/LXC if they still work.
- Verify bridge status/heartbeat and a real actuator acknowledgement.
- Verify dispatcher/failover/emergency dashboard.

## ESP32 failure only

- Use USB300 emergency control for mapped relay/cover commands.
- Replace/reflash ESP32 from the exact private hardware/firmware backup.
- Restore its LAN address and TCP port.
- Verify RS485 bidirectional feedback.
- Run a state-preserving primary-path test.

## Linux bridge failure

- Restore the LXC/VM image if available.
- Otherwise rebuild OS, virtual environment, bridge source, dependencies and systemd units.
- Verify MQTT and ESP32 connectivity.
- Start the bridge and local watchdog.
- Require a real bus acknowledgement before declaring recovery complete.

## USB300 failure

- Attach replacement transceiver.
- Configure its stable serial-by-id path.
- Read its Base ID.
- Decide whether to re-teach actuators or deliberately migrate the Base ID.
- Restore/generate the device file.
- Verify sensor receive.
- Verify one state-preserving relay TX and one cover STOP TX.

## Total rebuild order

```text
PCT14 / bus inventory
→ ESP32 TCP↔RS485
→ Linux bridge
→ MQTT + Home Assistant primary entities
→ FTR/F4HK translation and HVAC mode
→ USB300 receive
→ USB300 sender mappings
→ RF dispatcher
→ automatic failover
→ emergency dashboard
→ voice-assistant exposure if desired
→ acceptance tests
```

## Final acceptance checklist

- [ ] One primary bridge writer only
- [ ] ESP32 TCP reachable
- [ ] RS485 feedback observed
- [ ] Bridge online + heartbeat fresh
- [ ] No stuck pending commands
- [ ] No active bus warnings
- [ ] Lights/switches verified
- [ ] Covers verified
- [ ] Climate/F4HK values plausible
- [ ] EnOcean room controllers fresh
- [ ] USB300 receive verified
- [ ] USB300 Base ID documented
- [ ] RF relay TX verified
- [ ] RF cover STOP TX verified
- [ ] Normal primary command produces no RF duplicate
- [ ] Emergency dashboard works without normal FAM14 entity calls
- [ ] Home Assistant configuration valid

# FTR / F4HK climate notes

This section contains **field observations** from a real Eltako Series 14 installation. Verify against your hardware and Eltako/EnOcean documentation before controlling HVAC equipment.

## Typical data flow

```text
physical EnOcean room controller (FTR/FUTH class)
    │ A5-10-06 style telemetry
    ▼
USB300 → EnOcean-MQTT → bridge
    │ translate room → learned virtual sender
    ▼
F4HK/FHK actuator channel
    │ feedback on FAM14 bus
    ▼
bridge → MQTT → Home Assistant climate
```

## A5-10-06 room-controller values

Physical room controllers can provide target/setpoint and current temperature. Keep the physical sender ID and the virtual sender used toward F4HK as separate concepts.

## F4HK feedback frame observed

A repeatable F4HK feedback shape was observed as:

```text
A5 00 DB2 DB1 0F <sender-id> 30
```

For the observed installation:

```text
target_temperature_C = DB2 * 40 / 255
current_temperature_C = (255 - DB1) * 40 / 255
```

Examples:

| DB2 | Calculated target |
|---:|---:|
| 177 | 27.76 °C |
| 50 | 7.84 °C |
| 142 | 22.27 °C |

| DB1 | Calculated current |
|---:|---:|
| 105 | 23.53 °C |
| 107 | 23.22 °C |
| 109 | 22.90 °C |

This mapping matched simultaneous Home Assistant values in multiple independent observations.

## Bus-address feedback mapping

In one Series 14 installation, F4HK feedback sender IDs used a family where the final byte matched the FAM14 bus address in hexadecimal. Example only:

```text
bus 43 decimal = 0x2B -> feedback sender ...:2B
bus 44 decimal = 0x2C -> feedback sender ...:2C
```

Do not assume the full sender prefix is universal.

## Virtual sender mapping

A convenient deployment convention is to choose learned virtual room-controller sender IDs deterministically from the F4HK bus address, for example:

```text
virtual_sender_last_byte = bus_address_hex + 0x80
```

This is a deployment convention, not an EnOcean standard requirement. It makes recovery much easier if every mapping is generated rather than manually typed.

## Heating/cooling mode broadcast

A learned global H/K sender/function was observed using an RPS telegram with data byte `0x50` for cooling-mode refresh. The sender ID is site-specific and intentionally not published here.

Safety requirements:

- verify which F4HK/FHK modules have learned the H/K sender;
- send through the same serialized bus writer as all other FAM14 commands;
- refresh cooling only when the real heat-pump/plant mode is actually cooling;
- do not invent an opposite "heat" telegram if the installed Eltako logic uses timeout/absence of cooling refresh;
- fail closed if the global HVAC mode is ambiguous.

## USB300 limitation for climate failover

One USB300 Base-ID window may cover the virtual relay/cover senders but not the separate learned H/K sender. In that case, do **not** reprogram the USB300 Base ID dynamically. Use a second transmitter or re-teach the H/K sender under a controlled migration plan.


## References and provenance

For normative/product behavior, cross-check the current vendor/specification documentation linked in [`../SOURCES.md`](../SOURCES.md). The following public work was particularly useful when interpreting this installation:

- `grimmpp/home-assistant-eltako` for Series 14 climate/A5-10-06 implementation context;
- `grimmpp/eltako14bus` for Series 14 bus/protocol behavior;
- the Home Assistant Community Eltako Series 14 debugging thread for historical F4HK/A5-10-06 experiments;
- Eltako and EnOcean Alliance documentation for product/EEP definitions.

The byte formulas and sender/bus correlations above are retained as **field observations from this project's own captured values** unless explicitly identified as a specification statement.

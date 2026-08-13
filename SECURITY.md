# Security / privacy

## Before publishing a deployment fork

Do not commit:

- MQTT usernames/passwords,
- SSH passwords or private keys,
- Home Assistant long-lived access tokens,
- GitHub tokens,
- public DNS names that expose your private installation unless intentional,
- private household device inventory if you do not want it public,
- PCT14 exports containing identifiable sender mappings unless intentional.

Run:

```bash
python tools/sanitize_check.py
```

This scanner only catches obvious mistakes. It is not a substitute for GitHub secret scanning or manual review.

## Operational safety

A compromised MQTT broker or bridge can operate physical building actuators. Use a trusted LAN/VPN, strong authentication where supported, least privilege and regular backups.

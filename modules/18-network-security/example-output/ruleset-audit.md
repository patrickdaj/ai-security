<!-- Example output — illustrative deliverable of module 18. -->

# Firewall Ruleset Audit — `edge-fw01`

62 rules → 6 issues. Overall: perimeter is too flat; management ports exposed.

| Sev | Issue | Rule | Fix |
|---|---|---|---|
| critical | overexposed | `tcp dport 22 ip saddr 0.0.0.0/0 accept` | restrict to the bastion CIDR; move SSH behind the VPN |
| critical | overexposed | `tcp dport 5432 0.0.0.0/0 accept` | DB should never face the internet; allow only the app subnet |
| high | too_broad | `tcp dport 1-65535 ip saddr 10.0.0.0/8 accept` | replace the any-port allow with the 4 ports actually used |
| medium | shadowed | `... drop` after a broad `accept` | rule never matches; reorder or remove |
| low | dead | `accept` referencing a decommissioned host | delete |

## TLS (testssl.sh on the public endpoint)
TLS 1.0/1.1 enabled, weak ciphers present → generated a Mozilla "intermediate"
config (TLS 1.2+, AEAD ciphers, HSTS).

**Outcome:** a 62-rule ruleset → 6 prioritized issues with tightened
replacements, plus a hardened TLS config — the firewall review and transport
hardening a network security role owns.

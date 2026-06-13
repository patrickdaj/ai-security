# Module 18 — Network Security Engineering

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Architecture, Identity, Crypto, Network.** Module 05 was network
*analysis* and module 15 was zero-trust *policy*; this is the infrastructure
discipline — firewalls, segmentation, VPN, perimeter, and transport security.
Firewall rulesets rot into overexposure and dead rules nobody dares delete;
auditing them and designing segmentation are strong AI targets.

## Tools you tour

- **nftables / iptables / cloud security groups** — the rule engines.
- **WireGuard** — modern VPN; site-to-site and remote access.
- **Suricata / Zeek** (revisit) — IDS/IPS and NSM as enforcement/visibility.
- **Arkime** — full-packet capture and NDR at scale.
- **TLS / DNS security** — `testssl.sh`, DNSSEC, DoH/DoT, egress filtering.

### Tour tasks

```bash
nft list ruleset                      # dump the firewall ruleset to audit
testssl.sh https://target             # grade a TLS endpoint
wg showconf wg0                        # inspect a WireGuard tunnel
```

## AI augmentation: ruleset auditor + segmentation designer

Build a tool that ingests a firewall/security-group ruleset and returns an audit:
**overexposed rules** (`0.0.0.0/0` on sensitive ports), **dead/shadowed rules**,
overly-broad ranges, and a recommendation each. Extend it to design
**segmentation** from observed flows — which ties directly back to the ZTNA
microsegmentation build (module 15). See [`project/`](./project) /
[`reference/`](./reference).

## Exercises

1. Audit a real `nft`/security-group ruleset; flag the overexposed and dead rules
   and propose a tightened set.
2. Grade a TLS endpoint and generate the hardened config (ciphers, protocols, HSTS).
3. Design east-west segmentation for a 3-tier app from its observed flows; verify
   it doesn't break legitimate traffic (reuse module 15's approach).

## Done when

- You can audit a firewall ruleset down to a defensible, tightened set, harden
  transport security, and design segmentation grounded in real traffic.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [nftables wiki](https://wiki.nftables.org/) · [WireGuard](https://www.wireguard.com/)
- [Suricata docs](https://docs.suricata.io/) · [Arkime](https://arkime.com/)
- [testssl.sh](https://testssl.sh/) · [Mozilla TLS config generator](https://ssl-config.mozilla.org/)
- [NIST SP 800-41 (firewalls)](https://csrc.nist.gov/pubs/sp/800/41/r1/final) · [NIST SP 800-215 (zero-trust network)](https://csrc.nist.gov/pubs/sp/800/215/final)
- [Cloudflare Learning Center (networking)](https://www.cloudflare.com/learning/)

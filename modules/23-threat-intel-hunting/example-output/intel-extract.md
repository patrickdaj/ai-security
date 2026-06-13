<!-- Example output — illustrative deliverable of module 23. -->

# Intel Extract — "FIN-actor invoice campaign" report

**Summary:** Financially-motivated actor delivers macro-laden invoices, runs
encoded PowerShell, injects into `explorer.exe`, and beacons over HTTPS to a
small set of VPS hosts. Overlaps with the FIN-WS04 incident (module 22).

## Indicators (→ pushed to MISP)
| Type | Value | Context |
|---|---|---|
| domain | `inv-updates[.]info` | macro C2 staging |
| ip | `185.x.x.x` | HTTPS beacon, 60s |
| hash | `sha256:9f2a…` | injected loader |
| email | `billing@inv-updates[.]info` | sender |

## ATT&CK techniques (→ Navigator layer)
T1566.001, T1059.001, T1055, T1071, T1053.005

## Hunt hypotheses (→ run in the SIEM/notebook)
- Office processes spawning `powershell.exe -enc` in the last 30 days.
- RWX memory regions in `explorer.exe` across the fleet (Velociraptor).
- Scheduled tasks created within 5 min of a Word process.
- Outbound TLS to newly-registered `.info` domains with regular 60s intervals.

**Outcome:** a prose report → shareable structured intel + four testable hunts,
wired to detection (09) and emulation (capstone).

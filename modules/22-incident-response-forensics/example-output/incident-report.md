<!-- Example output — illustrative deliverable of module 22 (isolated lab image). -->

# Incident Report — FIN-WS04 compromise

**Severity:** high · **ATT&CK:** T1566.001, T1059.001, T1055, T1071

**Summary:** A malicious macro in an emailed document spawned PowerShell, which
injected into `explorer.exe` and beaconed to a rare external host. Credential
material was accessed before containment.

## Timeline (reconstructed from memory + super-timeline)
| Time (UTC) | Event |
|---|---|
| 13:02 | `winword.exe` opens `invoice.doc`; child `powershell.exe -enc …` |
| 13:02 | `malfind` shows injected RWX region in `explorer.exe` (T1055) |
| 13:03 | Outbound TLS to `185.x.x.x:443`, 60s beacon (T1071) |
| 13:07 | `lsass` handle opened by injected thread (credential access) |
| 13:31 | Host isolated (NetworkPolicy deny-egress); memory captured |

## Root cause
Macro execution was enabled; no attachment sandboxing on the mail path.

## Containment / next
Isolated and imaged. Rotate FIN-WS04 + any creds used post-13:07. Block the C2
host org-wide (feed to module 09 as a Sigma rule). Disable macros from email via
GPO. YARA rule for the injected stub written and pushed to the fleet.

**Outcome:** thousands of artifact rows → a defensible timeline, root cause,
containment plan, and report — each line traceable to a Volatility/plaso entry.

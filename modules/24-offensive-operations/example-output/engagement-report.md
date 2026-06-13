<!-- Example output — illustrative deliverable of module 24 (authorized lab AD). -->

# Red-Team Engagement — lab.local (authorized lab range)

**Result:** foothold → Domain Admin in 4 hops.

| # | Principal | Technique enabling next hop |
|---|---|---|
| 1 | `lowpriv@lab.local` | Kerberoast `svc-sql` (weak SPN password) |
| 2 | `svc-sql` | local admin on `SQL01`; dump creds → `helpdesk` |
| 3 | `helpdesk` | `GenericAll` on the `Servers` OU (AD ACL abuse) |
| 4 | `helpdesk` (escalated) | DCSync → `krbtgt` hash → Domain Admin |

**Narrative & next move at each step** generated from the BloodHound graph;
DCSync was the final move once `helpdesk` held replication rights.

## Blue-team fixes (→ handed to detection 09/21)
- Hop 1: set a 25+ char password on `svc-sql`; alert on Kerberoast (4769 RC4).
- Hop 3: remove `GenericAll`; alert on ACL modifications to privileged OUs.
- Hop 4: alert on DCSync from non-DC hosts (1644 / directory replication).

## OPSEC notes
Sliver beacon over HTTPS, 90s jitter, named-pipe pivot for lateral movement —
documented the telemetry each choice generated so the SOC can build coverage.

**Outcome:** full kill chain narrated with next moves, an engagement report, and
the exact detections that would have caught each hop — purple from both sides.

<!-- Example output — the anomaly half of microseg.py run against
     project/sample_flows.json. These observed flows were deliberately NOT
     turned into allow rules. -->

# Microsegmentation Anomalies — `prod`

Two observed flows were flagged as "happened, but should not be allow-listed."
They are candidate incidents, not policy.

## HIGH — `payments -> 169.254.169.254:80 /latest/meta-data/iam/security-credentials/`
The `payments` workload reached the **cloud instance metadata endpoint**, on the
IAM credentials path. This is the classic SSRF → credential-theft pattern (steal
the node/role credentials, then pivot in the cloud control plane). Do **not**
allow-list it.
- **Action:** require IMDSv2 (hop limit 1), block egress to `169.254.169.254`
  from workloads via an egress policy, and audit `payments` for an SSRF sink.
- **Cross-link:** feed this to module 11 — the stolen role may open an attack path.

## MEDIUM — `analytics -> postgres:5432`
The `analytics` identity touched the **production database** (40 flows). Analytics
should read from a replica or a warehouse, not prod Postgres. Excluded from the
`allow-to-postgres` policy.
- **Action:** confirm with the data team; if illegitimate, it stays denied by
  default-deny. If legitimate-but-wrong-target, repoint analytics at the replica.

---

**Outcome:** the synthesized policy set encodes only the legitimate flows; the
two suspicious ones surface as triage items instead of being silently baked into
the allow-list — which is exactly the failure mode of naive "learn from traffic"
microsegmentation.

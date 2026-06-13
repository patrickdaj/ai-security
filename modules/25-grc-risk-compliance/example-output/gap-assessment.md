<!-- Example output — illustrative deliverable of module 25. -->

# SOC 2 Gap Assessment — from the curriculum's own findings

Evidence from modules 01/03/08/11/19 mapped to SOC 2 Trust Services Criteria.

| Status | Control | Evidence / finding |
|---|---|---|
| violated | CC6.1 (logical access) | over-permissioned `ci-deploy` IAM role (module 11) |
| violated | CC6.1 | public S3 bucket leaking a key (module 08/11) |
| satisfied | CC7.2 (monitoring) | runtime detection + alert triage (modules 09/13/21) |
| satisfied | CC8.1 (change mgmt) | signed artifacts + provenance (module 12) |
| no_evidence | CC6.6 (encryption in transit) | no TLS posture evidence yet → run module 18 |
| no_evidence | CC1.4 (background/access reviews) | run module 19's access review |

## Top gaps (prioritized)
1. **Logical access (CC6.1)** — two open violations; remediate the IAM role + bucket.
2. **Encryption evidence (CC6.6/CC6.7)** — produce the module 18/20 outputs.
3. **Access reviews (CC1.4)** — schedule the module 19 review quarterly.

## Risk narrative (one gap, FAIR-style)
The public bucket + leaked key: loss-event frequency *moderate* (internet-facing,
trivially discoverable), magnitude *high* (the key reaches all secrets). Residual
risk: **high** until the bucket is private and the key rotated.

**Outcome:** the whole curriculum's output → a framework-mapped gap assessment
with prioritized gaps and a business-terms risk narrative — the audit story.

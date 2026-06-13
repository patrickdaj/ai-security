<!-- Example output — illustrative deliverable of module 17. -->

# Threat Model — the curriculum's automation pipeline

**Assets:** the `ANTHROPIC_API_KEY`, scan reports (may contain findings/secrets),
the CodeBuild role, the report S3 bucket.
**Trust boundaries:** GitHub → CodeBuild; CodeBuild → Anthropic API; CodeBuild →
S3; the scanned target's code (untrusted input) → the pipeline.

| STRIDE | Where | Threat | Sev | Control |
|---|---|---|---|---|
| Info disclosure | report → S3 | Reports leak secrets/findings if bucket is public | high | block public access + KMS (already done); redact secrets (gitleaks adapter does) |
| Elevation | CodeBuild role | Over-broad role lets a poisoned build pivot | high | least-priv IAM (logs + one bucket + one secret) |
| Tampering | GitHub → build | Malicious PR alters the buildspec to exfil the key | high | run on `pull_request` (no secrets for forks); pin actions |
| Spoofing | CodeBuild → API | Stolen key used elsewhere | medium | key in Secrets Manager, never in env/logs; rotate |
| DoS | scheduled build | Runaway scan exhausts minutes/cost | low | timeouts + budget alarms |

**Outcome:** a design → assets, boundaries, STRIDE threats, and a control each —
the artifact you take into a design review, generated from the description and
refined by you.

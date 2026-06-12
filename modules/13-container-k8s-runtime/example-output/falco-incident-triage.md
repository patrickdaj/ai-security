<!-- Example output — illustrative deliverable of module 13 (runtime-alert
     triage). Shows how a Falco firehose collapses into incidents. -->

# Falco Runtime Triage — `prod` cluster (15-minute window)

Source: 1,284 Falco alerts → deduplicated by root cause with `aug`. **3
incidents** (1 real), 1,281 alerts collapsed into benign clusters.

## INCIDENT — Reverse shell in `payments` pod (TRUE POSITIVE, conf 0.93)
- **dedup_key:** `payments/sh->/dev/tcp`
- **Collapsed alerts:** 4
- **ATT&CK:** T1059.004 (Unix Shell) → T1071 (C2)
- **Summary:** `sh -i` spawned by the `payments` container's Java process,
  writing to `/dev/tcp/185.x.x.x/4444`. The parent is the request-handler
  thread — consistent with exploitation of a deserialization bug, not an
  operator shell.
- **Next step:** isolate the pod (NetworkPolicy deny-egress), snapshot, and
  pull the JVM thread dump; check `payments` for the CVE from module 03.

## Benign clusters (deduped, no action)

| dedup_key | Alerts | Verdict | Why |
|-----------|-------:|---------|-----|
| `*/apt-get->write /var/lib` | 902 | false_positive | Base-image package cache updates on rollout. |
| `*/sed->write /etc/hosts` | 379 | false_positive | Init container templating /etc/hosts; expected. |

**Outcome:** 1,284 alerts → 1 real incident with an ATT&CK mapping and a
containment step. The 1,281 benign alerts collapse to two named clusters you
acknowledge once.

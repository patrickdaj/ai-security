<!-- Example output — the n8n SOAR build: an alert routed by the AI verdict. -->

# SOAR run — AI-routed alert triage (n8n + aug)

A SIEM forwards an alert to the n8n webhook; the workflow calls the `aug` triage
service and routes on the returned verdict. No human touches a false positive.

## Alert in (webhook POST)
```json
{
  "rule_id": "EncodedCommand on FIN-WS04",
  "title": "PowerShell -enc launched by winword.exe",
  "severity": "high",
  "host": "FIN-WS04",
  "context": "parent=winword.exe; child=powershell.exe -enc <b64>; egress 185.x:443 60s beacon"
}
```

## Triage service returns (typed)
```json
{
  "verdict": "true_positive",
  "adjusted_severity": "high",
  "confidence": 0.93,
  "rationale": "Office-spawned encoded PowerShell with periodic external beacon — classic macro→C2.",
  "next_step": "Isolate FIN-WS04; pull JVM/thread context; rotate creds used after t0."
}
```

## n8n routes by `verdict`
| Verdict | Branch | Action node (replace with your tooling) |
|---|---|---|
| `true_positive` | → Notify + open ticket | Slack `#soc` + Jira incident, severity-mapped |
| `false_positive` | → Suppress + log | tuning note, no page |
| `needs_review` | → Queue for analyst | Tier-2 queue |

**This run:** routed to **Notify + open ticket** → Slack alert posted, incident
opened, host-isolation playbook queued (gated on analyst confirm for the
irreversible step).

**Outcome:** the same "AI is the judgment layer, humans gate the irreversible"
pattern as the Python pipeline — but as a low-code n8n SOAR flow any analyst can
read and extend. The verdict is produced by the `aug` engine; n8n only routes.

<!-- Example output — illustrative deliverable of module 21. -->

# SecOps Deliverable — detection + alert triage

## 1. Generated detection (intent → EQL)
Intent: *"PowerShell launched by an Office app with an encoded command."*
```eql
process where event.type == "start"
  and process.name == "powershell.exe"
  and process.parent.name in ("winword.exe", "excel.exe", "outlook.exe")
  and process.args : "*-enc*"
```
Validated: fires on the Atomic Red Team T1059.001 sample, silent on a benign
admin script. Same intent in SPL/KQL generated alongside.

## 2. Alert triage (one shift)
1,240 alerts → triaged. **2 incidents**, 1,238 deduped/benign.

| Alert | Verdict | Sev | Why (enrichment) | Next (SOAR) |
|---|---|---|---|---|
| EncodedCommand on FIN-WS04 | true_positive | high | parent=winword, child beaconed to rare host | isolate host + ticket |
| 4625 spike svc-backup | false_positive | info | scheduled job, known source IP, succeeded after | suppress + tune |
| 900× "PsExec" SOC tools | false_positive | info | from the admin jump box, expected | allowlist source |

**Outcome:** intent → validated detection on a real backend, and a 1,240-alert
queue collapsed to 2 real incidents with enrichment and a response action each.

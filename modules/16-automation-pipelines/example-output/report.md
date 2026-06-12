<!-- Example output — what `python -m automation` writes to report.md.
     Illustrative; run the pipeline to generate a live one. -->

# Security Pipeline Report — `.`

Generated 2026-06-12T06:00:11+00:00 · 34 findings · triaged with `aug`

| Severity | Count |
|----------|------:|
| critical | 1 |
| high | 3 |
| medium | 8 |
| low | 22 |

## [critical] trivy: CVE-2021-44228
- **Location:** `log4j-core@2.14.1`
- **Verdict:** true_positive (severity critical → critical, conf 0.96)
- **Why:** reachable via a user-controlled logging path; default lookups enabled.
- **Fix:** upgrade to 2.17.1.

## [high] semgrep: python.lang.security.audit.subprocess-shell-true
- **Location:** `app/jobs.py:130`
- **Verdict:** true_positive (severity high → high, conf 0.9)
- **Why:** authenticated filename interpolated into `shell=True`.
- **Fix:** drop shell=True, pass an arg list.

*(31 more, sorted by adjusted severity…)*

**Pipeline exit code: 1** (a finding met `--fail-on critical`) — the build gates.

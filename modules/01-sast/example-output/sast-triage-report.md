<!-- Example output — an illustrative deliverable of this module's project
     (triage_sast.py). Hand-authored as a reference for what the tool produces;
     run it against your own Semgrep results to generate live reports. -->

# SAST Triage Report — `vuln-app`

Source scan: `semgrep --config=auto` (47 raw findings) → triaged with `aug`.
**11 kept** after confidence gate (`--min-confidence 0.7`); 36 suppressed as
false positives or low-confidence noise.

## Kept findings

### 1. SQL injection via string formatting — TRUE POSITIVE
- **Rule:** `python.lang.security.audit.formatted-sql-query`
- **Location:** `app/db.py:42`
- **Severity:** medium → **high** (conf 0.94)
- **Why:** `username` flows unsanitized from the `/login` request body
  (`app/views.py:88`) into a `%`-formatted query. Reachable pre-auth.
- **Exploitability:** `' OR '1'='1` style auth bypass; classic UNION exfil.
- **Fix:**
  ```diff
  - cur.execute("SELECT * FROM users WHERE name = '%s'" % username)
  + cur.execute("SELECT * FROM users WHERE name = %s", (username,))
  ```

### 2. Command injection in archive handler — TRUE POSITIVE
- **Rule:** `python.lang.security.audit.subprocess-shell-true`
- **Location:** `app/jobs.py:130`
- **Severity:** high → **critical** (conf 0.91)
- **Why:** `filename` from an authenticated upload is interpolated into
  `subprocess.run(..., shell=True)`. Reachable by any logged-in user.
- **Fix:** drop `shell=True`, pass an arg list, and validate the path.

## Suppressed (sample of 36)

| Rule | Location | Verdict | Why |
|------|----------|---------|-----|
| `tainted-html-string` | `app/templates.py:14` | false_positive (0.88) | Input is a hardcoded enum, not user-controlled. |
| `weak-random` | `app/ids.py:9` | false_positive (0.82) | Used for a cache key, not a security token. |
| `hardcoded-password` | `tests/fixtures.py:5` | false_positive (0.90) | Test fixture, not a real credential. |

**Outcome:** 47 → 11 actionable, each with a concrete fix and a reachability
rationale grounded in the call sites — the analyst reviews 11, not 47.

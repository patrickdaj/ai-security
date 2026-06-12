<!-- Example output — the flagship deliverable of the capstone copilot: a
     prioritized, CROSS-CORRELATED report. Illustrative reference. -->

# Security Copilot Report — `vuln-app` + `acme-prod`

One run: SAST (01), secrets (02), SBOM/CVEs (03), web scan (04), and cloud
identity (11), normalized, triaged, and **correlated across tools**. 600+ raw
findings → **3 correlated risks** ranked by combined exposure.

## ① CRITICAL — Reachable RCE chained to an over-permissioned role
Correlates **3 findings** that are far worse together than apart:
- **SAST (01):** command injection in `app/jobs.py:130` (reachable by any user).
- **Supply chain (03):** `log4j-core@2.14.1` Log4Shell, reachable pre-auth.
- **Cloud identity (11):** the pod runs as `role/app-runtime`, which can
  `secretsmanager:GetSecretValue` on **all** secrets.

**Combined narrative:** either code path gives RCE in the pod; the pod's role
then reads every secret in the account. The fix order is RCE first
(patch log4j + remove `shell=True`), then scope `app-runtime` to its 3 secrets.

## ② HIGH — Public bucket leaks a key into a privilege path
- **Secrets (02):** AWS access key in `acme-public-assets/terraform.tfstate`.
- **Cloud identity (11):** that key belongs to a role on the Path-2 escalation.
**Action:** make the bucket private, rotate the key, enable state encryption.

## ③ MEDIUM — Exposed `.git/config` on the web tier
- **Web scan (04):** `/.git/config` returns 200 (Nuclei template from module 04).
**Action:** block dotfiles at the proxy; confirm the full `.git` dir isn't served.

---

## Prioritization rationale (auditable)
Every rank traces to evidence: ① is critical because reachability (01/03) **and**
blast radius (11) are both confirmed; ② is high because a real credential sits on
a real escalation path; ③ is medium — real exposure, low blast radius. The
correlation is the value: three "mediums" in separate tools were one critical.

**Outcome:** 600+ findings across five tools → 3 ranked, cross-correlated risks
with an ordered fix plan you can hand to engineering.

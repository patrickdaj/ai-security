<!-- Example output — illustrative deliverable of module 11 (attack_paths.py).
     Hand-authored reference for what the IAM attack-path finder produces. -->

# Cloud Identity Attack-Path Report — `acme-prod` (AWS)

Source: Cartography graph + PMapper privesc enumeration → ranked & explained
with `aug`. 18 candidate edges → **2 high-severity end-to-end paths**.

## Path 1 — CI role to account admin (CRITICAL, conf 0.92)

**Entrypoint:** `role/ci-deploy` (assumable by the GitHub Actions OIDC provider)
**Target:** `role/OrganizationAdmin`

| # | Principal | Edge that enables the next hop |
|---|-----------|--------------------------------|
| 1 | `role/ci-deploy` | `iam:CreatePolicyVersion` on a policy attached to itself |
| 2 | `role/ci-deploy` (escalated) | `iam:PassRole` + `lambda:CreateFunction` |
| 3 | `lambda/exfil` | assumes `role/OrganizationAdmin` via `sts:AssumeRole` |

**Narrative:** the CI role can rewrite its own policy (`CreatePolicyVersion`),
grant itself `PassRole`, deploy a Lambda running as a privileged role, and from
there assume `OrganizationAdmin`. A leaked OIDC trust or a malicious PR that
reaches the deploy workflow walks straight to account takeover.

**Minimal fix that breaks the path:** remove `iam:CreatePolicyVersion` from
`ci-deploy` (it never legitimately rewrites policies) — cuts the path at hop 1.

## Path 2 — Public S3 read to secrets (HIGH, conf 0.81)

**Entrypoint:** unauthenticated (bucket `acme-public-assets` allows `s3:GetObject` to `*`)
**Target:** `secretsmanager` values

**Narrative:** the public bucket contains a Terraform state file with a
hardcoded access key for `role/app-runtime`, which holds
`secretsmanager:GetSecretValue` on all secrets. Anyone on the internet → app
secrets.

**Minimal fix:** make the bucket private and rotate the leaked key; scope
`app-runtime` to the three secrets it actually reads.

---

**Outcome:** 18 graph edges → 2 explained, end-to-end attack paths, each with
the single least-privilege change that breaks it — the thing you take to the
cloud team, not a wall of permission diffs.

<!-- Example output — deliverable of the capstone purple_loop.py run in dry-run
     over sample_cloudtrail.json. Illustrative reference. -->

# Cloud Purple-Team Report — `acme-staging`

Loop: AI planned Stratus techniques → (dry-run) detonation → AI detection check
→ Sigma synthesis for gaps. 5 techniques emulated, **2 detection gaps closed**.

| Technique | Tactic | Detected? | Outcome |
|-----------|--------|-----------|---------|
| `aws.persistence.iam-create-admin-user` | Persistence | **MISSED** (0.88) | Gap → new Sigma rule |
| `aws.exfiltration.ec2-share-ebs-snapshot` | Exfiltration | **MISSED** (0.81) | Gap → new Sigma rule |
| `aws.credential-access.ec2-get-password-data` | Credential Access | detected (0.79) | GuardDuty covers it |
| `aws.defense-evasion.cloudtrail-stop` | Defense Evasion | detected (0.90) | Existing alert fired |
| `aws.discovery.ec2-enumerate-from-instance` | Discovery | detected (0.72) | Covered by anomaly rule |

## Gap 1 — IAM admin user created, undetected
The `CreateUser` → `AttachUserPolicy(AdministratorAccess)` sequence produced no
alert. **Synthesized:** [`iam-create-admin-user.sigma.yml`](../../09-detection-engineering/example-output/iam-create-admin-user.sigma.yml)
(also the module-09 example) — keys on `AttachUserPolicy` with the
AdministratorAccess ARN. Validated with `sigma check`, converts to the SIEM.

## Gap 2 — EBS snapshot shared cross-account, undetected
`ModifySnapshotAttribute` adding an external account to `createVolumePermission`
went unflagged — a quiet exfiltration path. A Sigma rule keying on that event +
an unknown target account id was generated and queued for review.

---

**Outcome:** offense found two blind spots; the copilot wrote the detections
that close them. The detonation step is gated — live runs require explicit
authorization (`--live --i-am-authorized`, `STRATUS_ALLOW=1`); this run was
dry-run over recorded CloudTrail.

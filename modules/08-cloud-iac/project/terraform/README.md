# Misconfigured Terraform — scan target

**DELIBERATELY VULNERABLE. Do not `terraform apply` this in a real account.**
It exists to be *scanned*, and to give modules 08 and 11 a realistic target.

```bash
checkov -d .          # policy-as-code findings
tfsec .               # Terraform misconfig
trivy config .        # IaC scan
```

Then run the augmentation pipeline's remediation build (module 08) against the
findings, or point your CIEM tooling (module 11) at the IAM here.

## Planted issues → what should catch them

| Resource | Issue | Catches | Curriculum link |
|----------|-------|---------|-----------------|
| `aws_s3_bucket.public_assets` + access block | public-read, no encryption/versioning | Checkov CKV_AWS_18/20/53… | module 11 path-2 leaky bucket |
| `aws_security_group.open_ssh` | SSH from `0.0.0.0/0` | tfsec ec2-no-public-ingress | — |
| `aws_iam_role_policy.ci_deploy_privesc` | `iam:CreatePolicyVersion`/`PassRole`/`AssumeRole` on `*` | Checkov IAM, PMapper | module 11 path-1 CI→admin |

The point: feed these findings to `aug` and watch it explain the attack and emit
a remediation diff — the same loop the real automation runs in CI.

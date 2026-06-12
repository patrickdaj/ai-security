# Terraform — scheduled scan pipeline

Provisions the headless `automation` pipeline as a **cron job in AWS**:
EventBridge → CodeBuild → encrypted S3 report bucket. This is how you run the
curriculum's augmentation pipeline unattended against a repo.

> **Real, billable resources. Apply in a sandbox account.** Review the plan
> first. Nothing here is a vulnerable target (that's `modules/08/project/terraform`) —
> this is production-style automation, hardened by design.

## What it creates

- **S3 report bucket** — KMS-encrypted, versioned, public access fully blocked.
- **CodeBuild project** — clones `repo_url`, installs Semgrep/Trivy/Gitleaks,
  runs `python -m automation`, uploads `report.md` / `report.json` to S3 under a
  per-run timestamp prefix.
- **EventBridge rule** — fires the build on `schedule_expression` (default: daily
  06:00 UTC).
- **Least-privilege IAM** — the build role gets only logs, `s3:PutObject` to the
  report bucket, and (if triage is enabled) `secretsmanager:GetSecretValue` on
  the one secret.

## Usage

```bash
cd terraform/automation
terraform init
terraform apply \
  -var 'repo_url=https://github.com/patrickdaj/ai-security' \
  -var 'repo_branch=main' \
  -var 'anthropic_secret_arn=arn:aws:secretsmanager:...:secret:anthropic-api-key'
```

Omit `anthropic_secret_arn` to run **aggregation-only** (no model, no key) — the
build passes `--no-triage` automatically.

## Notes

- The API key is injected from Secrets Manager as a CodeBuild env var of type
  `SECRETS_MANAGER`; it never appears in the Terraform state or the buildspec.
- Public GitHub repos clone without credentials. For a private repo, register a
  CodeBuild source credential (GitHub PAT) or switch the source to a CodeStar
  connection.
- `fail_on` controls the build's exit code; a failing build is visible in the
  CodeBuild console and CloudWatch, and the report still uploads.

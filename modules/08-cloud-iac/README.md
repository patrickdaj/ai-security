# Module 08 — Cloud & Infrastructure-as-Code

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


Cloud/IaC scanners check Terraform, CloudFormation, Kubernetes, and live cloud
config against best-practice policies. They tell you *what's wrong* precisely and
leave you to figure out *the exact fix in your codebase* — which is where AI
turns a finding into an applied, context-aware remediation.

## Tools you tour

- **Checkov** — policy-as-code scanner for IaC (Terraform, CFN, K8s, Dockerfile).
- **tfsec / Trivy config** — fast Terraform-focused misconfig detection.
- **Prowler** — assesses a *live* AWS/Azure/GCP account against CIS benchmarks.
- **kube-bench** — checks a cluster against the CIS Kubernetes benchmark.

### Tour tasks

```bash
checkov -d modules/08-cloud-iac/project/terraform --output json > scratch/checkov.json
tfsec modules/08-cloud-iac/project/terraform --format json > scratch/tfsec.json
# Prowler/kube-bench need a real account/cluster — read their output formats.
```

Write a small misconfigured Terraform module (public S3 bucket, open security
group) under `project/terraform/` and scan it. Each finding names a resource and
a policy — but the fix lives in *your* HCL, with *your* variables.

## AI augmentation: remediation-as-code generator

Build a tool that, for each Checkov/tfsec finding, reads the offending IaC
*file* (not just the line), and generates a minimal patch that satisfies the
policy while preserving the surrounding config and style — emitted as a unified
diff you can review and apply.

Map findings to `Finding`s with the relevant HCL block in `.context`, and extend
the triage to produce a `Remediation { diff, breaking_change_risk, explanation }`.
The breaking-change flag is the gate: auto-apply low-risk fixes (add a tag,
tighten a CIDR), hold high-risk ones (change an IAM policy) for human review.

## Exercises

1. Generate diffs for a handful of Checkov findings and apply the safe ones to a
   scratch branch; re-scan to confirm they clear.
2. Add Terraform-aware context: include `variables.tf` so the model uses your
   variables instead of hardcoding values.
3. For Prowler live-account findings, generate the remediation as both a console
   click-path *and* the IaC change, so the fix is durable.

## Done when

- You can take an IaC scan and produce review-ready diffs that actually clear the
  findings on re-scan, with risky changes correctly held back for human sign-off.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Checkov](https://www.checkov.io/)
- [Trivy (config/IaC, incl. tfsec)](https://trivy.dev/)
- [Prowler](https://github.com/prowler-cloud/prowler)
- [kube-bench](https://github.com/aquasecurity/kube-bench)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)

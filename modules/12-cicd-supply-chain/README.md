# Module 12 — CI/CD & Artifact Integrity

Phase: **Infrastructure & Runtime.** Your pipeline is infrastructure with write
access to production and a hoard of secrets. Attackers know it: poisoned
pipeline execution, leaked `GITHUB_TOKEN`, dependency confusion, unsigned
artifacts. The tools here audit pipeline config and establish artifact
provenance; AI reads the config the way an attacker would and generates the
hardening.

## Tools you tour

- **zizmor** / **octoscan** — static analysis for GitHub Actions workflows
  (the highest-density source of CI vulns).
- **StepSecurity Harden-Runner** — egress control + runtime monitoring for CI.
- **Sigstore / cosign** — keyless artifact signing and verification.
- **SLSA / in-toto** — provenance framework: prove *how* an artifact was built.
- **Conftest / Terrascan** — policy gates run *inside* the pipeline.

### Tour tasks

```bash
zizmor .github/workflows/            # audit your own workflows
cosign sign --yes <image>            # keyless signing
cosign verify <image> --certificate-identity ...   # verification
```

Read a zizmor finding (e.g. a workflow that runs untrusted PR code with secrets
in scope). Each is a precise pattern; the *fix in your specific workflow* — and
why it matters — is what the model adds.

## AI augmentation: pipeline auditor + provenance generator

Two builds:

1. **Pipeline auditor.** Normalize zizmor/octoscan findings into `Finding`s with
   the offending workflow block in `.context`, and use the triage engine to
   explain the attack (e.g. "this `pull_request_target` + checkout of PR head
   exposes your secrets to fork code") and emit a `Remediation` diff that fixes
   it without breaking the workflow.
2. **Provenance setup generator.** Given a repo's build, generate the cosign +
   SLSA provenance wiring (signing step, verification gate) as a workflow patch,
   plus the policy that rejects unsigned artifacts at deploy.

The gate: the auditor proposes diffs; you review and apply. Never let the tool
that hardens the pipeline auto-merge to a protected branch.

## Exercises

1. Audit a deliberately vulnerable workflow (a `pull_request_target` with secret
   access) and confirm the model explains the exfil path and patches it.
2. Generate the cosign signing + verification steps and prove an unsigned image
   is rejected by your Conftest/policy gate.
3. Add a dependency-confusion check: flag internal package names that could be
   shadowed on a public registry, and generate the scoping fix.

## Done when

- You can take a repo's `.github/workflows/`, produce review-ready hardening
  diffs for the real issues, and stand up signing + provenance so unsigned
  artifacts can't deploy.

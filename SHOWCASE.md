# Showcase — what this curriculum produces

A portfolio index of the concrete deliverables each module's AI augmentation
emits. These are the artifacts you'd put in front of a hiring manager, a client,
or a security review board.

> **About these files:** each linked artifact is an *illustrative reference
> output* — hand-authored to show the shape and quality of what the module's
> project produces, so the repo has something to show before you run anything.
> Run each project against your own authorized targets (with the Claude or
> local Ollama backend) to generate live results. They live under each module's
> `example-output/`; live runs write to the gitignored `scratch/`.

## Deliverables

| Module | Deliverable | What it demonstrates |
|--------|-------------|----------------------|
| 01 SAST | [sast-triage-report.md](./modules/01-sast/example-output/sast-triage-report.md) | 47 findings → 11 actionable, false positives killed with reasons |
| 03 Supply chain | [reachability-report.md](./modules/03-supply-chain/example-output/reachability-report.md) | 312 CVEs → 2 reachable, with exploit narratives |
| 04 DAST | [git-config-exposure.nuclei.yaml](./modules/04-dast-web/example-output/git-config-exposure.nuclei.yaml) | advisory → a valid Nuclei detection template |
| 09 Detection | [iam-create-admin-user.sigma.yml](./modules/09-detection-engineering/example-output/iam-create-admin-user.sigma.yml) | threat intel → a tagged, convertible Sigma rule |
| 11 Cloud identity | [attack-path-report.md](./modules/11-cloud-identity-attack-paths/example-output/attack-path-report.md) | IAM graph → 2 end-to-end attack paths + least-priv fixes |
| 13 K8s runtime | [disallow-privileged.kyverno.yaml](./modules/13-container-k8s-runtime/example-output/disallow-privileged.kyverno.yaml) · [falco-incident-triage.md](./modules/13-container-k8s-runtime/example-output/falco-incident-triage.md) | NL intent → admission policy; 1,284 alerts → 1 incident |
| 15 ZTNA | [microseg-policies.yaml](./modules/15-zero-trust-ztna/example-output/microseg-policies.yaml) · [anomalies.md](./modules/15-zero-trust-ztna/example-output/anomalies.md) | observed traffic → default-deny Istio policies + flagged anomalies |
| ★ Capstone | [security-report.md](./modules/capstone/example-output/security-report.md) · [purple-team-report.md](./modules/capstone/example-output/purple-team-report.md) | 600+ findings → 3 cross-correlated risks; purple-team gap closure |

## Automation (the deliverables, generated unattended)

These artifacts aren't just hand-run — the same pipeline produces them headless:

- [`automation/`](./automation) — `python -m automation` / `aug-pipeline`: scan
  → triage → `report.md` + `report.json`, severity-gated exit code.
- [`.github/workflows/security-scan.yml`](./.github/workflows/security-scan.yml)
  — runs it on a schedule and uploads the report; the repo scans itself.
- [`terraform/automation/`](./terraform/automation) — the pipeline as a scheduled
  AWS job (EventBridge → CodeBuild → encrypted S3). Infra-as-code, hardened.
- [`modules/08-cloud-iac/project/terraform/`](./modules/08-cloud-iac/project/terraform)
  — a misconfigured module to scan (the target, not the automation).

## The throughline these show

Across every artifact: the deterministic tool produced *candidates*; the AI
applied the *judgment* (reachability, blast radius, dedup, correlation,
remediation); and anything irreversible (applying a fix, detonating an attack,
enforcing a policy) stays behind a human gate. That is the portfolio thesis —
an AI-augmented security engineer, not an AI that replaces one.

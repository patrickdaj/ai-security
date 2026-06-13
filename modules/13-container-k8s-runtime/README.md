# Module 13 — Containers & Kubernetes Runtime

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


Phase: **Infrastructure & Runtime.** Module 08 checked cluster config *before*
deploy. This module is about *runtime*: what's actually happening inside running
containers, and stopping bad things at the admission gate. Runtime tools emit a
firehose of low-context alerts; admission policy is tedious to write by hand.
AI helps with both.

## Tools you tour

- **Trivy** (revisited) — deep image + IaC + secret scanning.
- **Falco** — eBPF/syscall runtime detection ("shell spawned in a container",
  "write to /etc/passwd"). Rich rules, noisy output.
- **Tetragon** — eBPF runtime security observability + enforcement.
- **Kubescape** — posture + NSA/CIS framework scanning.
- **OPA Gatekeeper / Kyverno** — admission control: reject bad pods at apply.

### Tour tasks (against a kind/minikube cluster)

```bash
trivy image <image>
# Falco running in the cluster emits JSON alerts to stdout/sidecar
kubescape scan framework nsa
kyverno apply policy.yaml --resource pod.yaml   # test an admission policy
```

Watch Falco for a few minutes on a busy cluster. Most alerts are benign
(package managers, init scripts). Finding the real incident in the stream is the
analyst's pain — and the augmentation's job.

## AI augmentation: runtime-alert triage + admission-policy generator

Two builds:

1. **Runtime triage.** Ingest Falco/Tetragon alerts (with the process tree /
   syscall context) and return typed [`RuntimeIncident`](../../aug/models.py):
   verdict, severity, a `dedup_key` derived from *root cause* (so the 400 alerts
   from one cron job collapse to one), the likely ATT&CK technique, and the next
   investigative step.
2. **Admission-policy generator.** Given a natural-language intent ("no
   containers may run as root or mount the docker socket"), generate a
   [`PolicyDraft`](../../aug/models.py) — Kyverno or Rego — render it, and
   validate with `kyverno apply` / `conftest` against allow/deny fixtures.

## Exercises

1. Triage a Falco capture; verify the dedup collapses repetitive benign alerts
   and surfaces the planted malicious one (e.g. a reverse shell).
2. Generate a Kyverno policy from intent and prove it admits the good pod and
   rejects the bad one.
3. Close the loop with module 09: for a confirmed runtime incident, emit a Sigma
   rule so the SIEM also catches it.

## Done when

- You can turn a Falco firehose into a short, deduplicated incident list with
  next steps, and generate validated admission policies from plain-language
  intent.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Falco docs](https://falco.org/docs/)
- [Tetragon docs](https://tetragon.io/docs/)
- [Kyverno docs](https://kyverno.io/docs/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)

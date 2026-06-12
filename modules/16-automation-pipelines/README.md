# Module 16 — Security Automation & Pipelines

Phase: **Infrastructure & Runtime.** Everything you've built so far runs by hand.
This module is where *you* turn it into automation: a headless pipeline, a CI
gate, and Terraform that runs it on a schedule. The deliverable is a system that
scans, triages, and reports with no human in the loop — until the gate.

> **There is a working reference in this repo** — [`automation/`](../../automation),
> [`.github/workflows/`](../../.github/workflows), and
> [`terraform/automation/`](../../terraform/automation). Treat it the way you'd
> treat a worked solution: read it, run it, then **build the tasks below** to
> make it yours. The build is the point; the reference is there so you're never
> stuck and so the repo has live CI to extend.

## Learning objectives

- Wrap deterministic scanners as normalizing adapters behind one interface.
- Build a headless orchestrator with a **severity-gated exit code** (CI-ready).
- Gate a pull request on findings and surface them in the GitHub Security tab.
- Provision the whole thing as scheduled cloud infrastructure with Terraform.

## Tour the reference

```bash
make pipeline          # run the reference pipeline against .
make scan              # aggregation only (no model/key)
cat scratch/pipeline/report.md
```

Read, in order: `automation/scanners.py` (adapters → `Finding`),
`automation/pipeline.py` (orchestration + exit code), `automation/report.py`
(rendering), then the two workflows and `terraform/automation/main.tf`. Notice
the seams you'll extend: the scanner `REGISTRY`, the gate logic, the CI trigger,
the Terraform target.

## Build tasks (the project)

Two starter stubs live in [`project/`](./project); the rest you wire yourself.

1. **Add a scanner.** Complete [`project/checkov_adapter.py`](./project/checkov_adapter.py)
   so IaC misconfigurations (point it at module 08's Terraform target) flow
   through the same pipeline. Register it in `automation.scanners.REGISTRY`.
2. **Correlate across tools.** Complete [`project/correlate.py`](./project/correlate.py):
   join findings by file / package / endpoint and have the model assess combined
   risk — the capstone's "three mediums are one critical" insight, as code.
3. **Gate PRs.** Make `security-scan.yml` *fail the check* on a new
   high-confidence true positive (not just upload an artifact), and **emit SARIF**
   so findings appear in the repo's Security tab.
4. **Post a summary.** Have the pipeline write a PR comment with the triaged
   top findings (GitHub Actions `gh` or the API).
5. **Automate it in cloud.** Extend `terraform/automation/` — or write your own —
   to run the pipeline against *your* target on a schedule, and store a run
   history you can diff (drift: what's new since last scan).

## Exercises

1. Add a second scanner of your choice (e.g. `bandit`, `osv-scanner`) and confirm
   it normalizes cleanly into `Finding`.
2. Tune the gate: fail on `critical` in CI but `high` in the nightly job; prove
   both exit codes behave.
3. Make the nightly Terraform job diff against the previous run and only alert on
   *new* findings.

## Done when

- One command (and one scheduled job) scans a target, triages it, gates on
  severity, and produces a report — with at least one scanner *you* added and
  cross-tool correlation *you* built. The reference got you started; the working
  pipeline is yours.

# Hardcore AI Security Engineering Curriculum

A self-driven, project-heavy curriculum that tours the open-source security
engineering toolchain — SAST, fuzzing, RE, supply chain, detection
engineering, cloud, LLM security — and then **augments each tool with AI**.

The thesis: a modern security engineer does not just *run* tools. They
understand the tool's internals well enough to extend it, and they wire an LLM
(Claude) into the loop to do the judgment-heavy work the tool can't: triaging
findings, killing false positives, synthesizing detection rules, root-causing
crashes, and explaining decompiled code.

> This is a **learning scaffold**, not a product. Every module is a directory
> with a deep-dive README, hands-on labs against intentionally-vulnerable
> targets, and an "AI augmentation" build project that plugs into the shared
> [`aug/`](./aug) library.

---

## How it works

```
tour the tool  ──►  understand its model  ──►  build the AI augmentation
 (run it, read     (data model, where it    (wire Claude into the loop via
  its output)       is weak, what it can't   the `aug` library; ship a CLI
                    decide on its own)        or wrapper that adds judgment)
```

Each module ends with a concrete deliverable you commit to this repo. By the
end you have a portfolio of ~11 AI-augmented security tools and a capstone
"security copilot" that orchestrates several of them.

## Curriculum map

| # | Module | Tools you tour | What you build with AI |
|---|--------|----------------|------------------------|
| 00 | [Foundations & Lab](./modules/00-foundations) | Docker, DVWA, Juice Shop, threat modeling | The `aug` augmentation library + a safe lab |
| 01 | [SAST](./modules/01-sast) | Semgrep, CodeQL, Bandit | Auto-triage + fix-suggestion engine for SAST findings |
| 02 | [Secrets](./modules/02-secrets) | TruffleHog, Gitleaks | Secret validator/classifier that kills noise |
| 03 | [Supply Chain](./modules/03-supply-chain) | Syft, Grype, Trivy, OSV-Scanner | SBOM-driven reachability + risk-narrative generator |
| 04 | [DAST & Web](./modules/04-dast-web) | OWASP ZAP, Nuclei, sqlmap | Advisory → Nuclei template generator; scan triage |
| 05 | [Recon & Network](./modules/05-recon-network) | nmap, Zeek, Suricata | PCAP/scan summarizer + detection-rule drafter |
| 06 | [Fuzzing](./modules/06-fuzzing) | AFL++, libFuzzer, Atheris | Harness generator + crash triage/dedup/root-cause |
| 07 | [Reverse Engineering](./modules/07-reverse-engineering) | Ghidra, radare2, angr | Decompiled-function summarizer + rename suggester |
| 08 | [Cloud & IaC](./modules/08-cloud-iac) | Checkov, tfsec, Prowler, kube-bench | Remediation-as-code generator |
| 09 | [Detection Engineering](./modules/09-detection-engineering) | Sigma, Wazuh, Zeek | Threat-intel → Sigma rule synthesizer; alert triage |
| 10 | [LLM/ML Security](./modules/10-llm-security) | garak, PyRIT, promptfoo, Rebuff | Prompt-injection red-team + guardrail harness |
| ★ | [Capstone](./modules/capstone) | all of the above | An AI security copilot that orchestrates the toolchain |

Work the modules in order — later modules assume the `aug` patterns from
earlier ones — or jump straight to whatever tool you need today.

## The augmentation pattern

Every AI augmentation in this repo follows the same shape, implemented once in
[`aug/`](./aug):

1. **Normalize** the tool's native output into a common finding/event schema.
2. **Enrich** with surrounding context (the code, the packet, the diff).
3. **Reason** with Claude using *structured outputs* so the result is typed and
   machine-consumable, not prose you have to parse.
4. **Gate** — never auto-act on a destructive decision; surface confidence and
   keep a human in the loop for anything irreversible.

This mirrors real AppSec automation: the LLM is a judgment layer bolted onto
deterministic tooling, not a replacement for it.

## Getting started

```bash
# 1. Read the foundations module first — it sets up the lab and the aug library.
$EDITOR modules/00-foundations/README.md

# 2. Create a Python env and install the augmentation library.
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Configure your Claude API key.
cp .env.example .env   # then edit .env

# 4. Smoke-test the AI layer.
python -m aug.smoke
```

See [`modules/00-foundations`](./modules/00-foundations) for the full setup,
including the intentionally-vulnerable lab targets (run them **only** in an
isolated Docker network).

## A note on scope and ethics

Everything here is for **authorized** security work: your own lab, CTFs,
engagements you have written permission for, and defensive research. The
intentionally-vulnerable apps are designed to be attacked; do not point any of
these tools at systems you do not own or have explicit authorization to test.

## Repository layout

```
aug/                 Shared AI-augmentation library (Claude wrapper, schemas, triage)
labs/                Safe lab setup (docker-compose for vulnerable targets)
modules/             The curriculum, one directory per module
  00-foundations/    Lab + aug library deep dive
  01-sast/ ...       Tool tour + AI augmentation project
  capstone/          Orchestrated copilot
```

Each module's `project/` directory is where your code goes; the READMEs tell
you what to build and how to measure whether it works.

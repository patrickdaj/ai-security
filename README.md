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

### Phase: Infrastructure & Runtime

Modules 01–10 mostly secure *code and apps*. This phase secures the
*infrastructure* underneath — identity, the pipeline, the runtime, the hosts,
and the network — where the hard part is reasoning over graphs and telemetry,
which is exactly where AI augmentation pays off most.

| # | Module | Tools you tour | What you build with AI |
|---|--------|----------------|------------------------|
| 11 | [Cloud Identity & Attack Paths](./modules/11-cloud-identity-attack-paths) | Cartography, PMapper, Steampipe, ScoutSuite | IAM attack-path finder + least-privilege synthesizer |
| 12 | [CI/CD & Artifact Integrity](./modules/12-cicd-supply-chain) | zizmor, Harden-Runner, Sigstore/cosign, SLSA | Pipeline auditor + provenance generator |
| 13 | [Container & K8s Runtime](./modules/13-container-k8s-runtime) | Trivy, Falco, Tetragon, Kyverno | Runtime-alert triage + admission-policy generator |
| 14 | [Host Hardening & Compliance](./modules/14-host-hardening-compliance) | OpenSCAP, Lynis, InSpec, osquery | Remediation-as-code + compliance control mapper |
| 15 | [Zero Trust (ZTNA)](./modules/15-zero-trust-ztna) | Pomerium, OpenZiti, Teleport, SPIFFE/SPIRE, OPA, Istio | Least-privilege & microsegmentation policy synthesizer |

| # | Module | Tools you tour | What you build with AI |
|---|--------|----------------|------------------------|
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

## Backends: Claude or local (Ollama)

The augmentation layer is provider-agnostic behind one `AugClient`. Pick a
backend with `AUG_BACKEND`:

- **`anthropic` (default)** — Claude via the Anthropic SDK. What the modules are
  tuned for: adaptive thinking plus structured outputs give the sharpest
  judgments and the most reliable typed results. Start here.
- **`ollama`** — a model running locally via [Ollama](https://ollama.com). Opt
  in when **data residency** matters (you'd rather not send proprietary code,
  secret context, or a cloud IAM graph to an external API), when you're offline,
  or to cut cost. Local models are weaker at the structured security reasoning
  these augmentations lean on, so treat it as the privacy/cost lever, not the
  quality default.

```bash
# Claude (default)
export AUG_BACKEND=anthropic   # + ANTHROPIC_API_KEY

# Local model
pip install -e ".[local]"      # adds the ollama client
ollama pull llama3.1           # or qwen2.5 / mistral-nemo
export AUG_BACKEND=ollama AUG_OLLAMA_MODEL=llama3.1
```

Both honor the same schemas and the same grounding system prompt, so every
module works unchanged on either — and comparing Claude vs. a local model on the
same finding is itself a worthwhile exercise (see module 00).

## Getting started

```bash
# 1. Read the foundations module first — it sets up the lab and the aug library.
$EDITOR modules/00-foundations/README.md

# 2. Create a Python env and install the augmentation library.
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # add ".[dev,local]" to include the Ollama backend

# 3. Configure your backend + key (Claude by default, or local Ollama).
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

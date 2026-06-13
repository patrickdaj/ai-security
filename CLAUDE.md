# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## What this is

A project-driven, **AI-augmented security engineering curriculum**. Each module
tours an open-source security tool, then wires Claude into its loop to do the
judgment work the tool can't — triage, reachability reasoning, rule synthesis,
remediation. It is a **learning scaffold, not a product**: most module code is
intentionally left for the learner to build.

The throughline, applied everywhere — keep it in mind when extending anything:
**deterministic tools find candidates → AI supplies the judgment → humans gate
anything irreversible.**

## Repository layout

- `aug/` — shared AI-augmentation library. **Complete; treat it like a stdlib.**
  `AugClient`, the normalized schemas, the generic triage engine.
- `automation/` — headless `scan → normalize → triage → report` pipeline with a
  severity-gated exit code. Complete reference; runnable as `python -m automation`.
- `modules/NN-name/` — the curriculum (`00`–`25` plus `capstone`). Every module:
  - `project/` — **starter stubs the learner builds** (they raise
    `NotImplementedError` / carry TODOs).
  - `reference/` — worked, runnable solutions.
  - `example-output/` — the target artifact (illustrative, hand-authored).
  - `README.md` — tour → AI augmentation → exercises → done-when → Resources.
- `labs/` — intentionally-vulnerable targets (`docker-compose.yml`); **localhost only**.
- `terraform/automation/` — the pipeline as a scheduled AWS job (hardened).
  `modules/08-cloud-iac/project/terraform/` is a **deliberately-misconfigured
  scan target** — scan it, never `terraform apply` it.
- `docs/` + `mkdocs.yml` + `mkdocs_hooks.py` — MkDocs Material site, single-sourced
  from the module READMEs via the include-markdown plugin.
- `.github/workflows/` — `ci`, `links`, `security-scan`, `docs`.
- `ROADMAP.md` (gap→module map + progress board), `SHOWCASE.md` (deliverables
  index), `modules/CONVENTIONS.md` (the module structure contract).

## Conventions — follow these

**Shared infra vs. learner work.** `aug/` and `automation/` are complete shared
infrastructure — extend them. `modules/*/project/` is the learner's to build:
**keep the `NotImplementedError`/TODO stubs as stubs** — they are the assignment,
not a bug to fix. `reference/` holds the worked answer; `example-output/` is
illustrative (hand-authored, not a captured run).

**The `aug` library.** `AugClient.reason(prompt, schema)` returns a validated
Pydantic instance via **structured outputs**; `.text()` returns prose. Reuse the
shared schemas — `Finding`, `Triage`, `Severity`, `Remediation`, `PolicyDraft`,
`AttackPath`, `RuntimeIncident` — before defining module-local ones. Default
model is `claude-opus-4-8` with adaptive thinking; backend is Claude by default
or local Ollama via `AUG_BACKEND=ollama` (same schemas, same code). When writing
model code, use the Anthropic SDK + structured outputs — never hand-rolled
prompt scraping.

**Adding/editing a module** must keep the triad consistent: a `project/` stub, a
`reference/`, an `example-output/`, plus a README with the Codespaces badge, a
tools tour, an AI-augmentation section, exercises, a done-when, and a Resources
list. Then add `docs/modules/NN-name.md` (an include stub), a nav entry in
`mkdocs.yml`, and a row in the README curriculum map. **Module numbers ascend
with phase order.**

**Docs are single-sourced.** Module READMEs are the source of truth; `docs/*.md`
are thin `{% include-markdown %}` stubs. `mkdocs_hooks.py` rewrites repo links
(to code, to other modules) so they resolve in the built site — **don't
duplicate content into `docs/`.**

**Links must resolve.** Relative links are validated **offline in CI** — every
`[text](path)` must point to a real file. External URLs are checked weekly. Keep
them valid.

**Style.** Python: `ruff`, line length 100 (`modules/*/project` is excluded, so
stubs may carry unused "hint" imports). Terraform: keep `terraform fmt` clean.
Markdown: match the surrounding module's tone.

## Commands

```
make setup        # pip install -e ".[dev]"   (add ".[dev,local]" for Ollama)
make smoke        # exercise the AI layer (needs a backend/key)
make lint         # ruff over aug/ and automation/
make test         # pytest
make pipeline     # headless scan + AI triage against .
make scan         # pipeline, aggregation only (no model/key needed)
make docs         # mkdocs build       (docs-serve serves at :8000)
make tf-fmt / tf-validate
make lab-up / lab-down
mkdocs build --strict     # the docs gate CI enforces
```

CI: `ci.yml` runs ruff + pytest + terraform validate + `mkdocs build --strict`;
`links.yml` runs offline link checks on PRs and a full external check weekly;
`security-scan.yml` dogfoods the pipeline against this repo; `docs.yml` deploys
the site to `gh-pages` on push to `main`.

## Configuration

Copy `.env.example` → `.env`. Set `ANTHROPIC_API_KEY` for the Claude backend, or
`AUG_BACKEND=ollama` for a local model. Optional extras: `.[local]` (Ollama),
`.[docs]` (MkDocs).

## Ethics & safety — non-negotiable

Everything targets systems you own or are explicitly authorized to test; the
vulnerable labs are localhost-only. The offensive, IR/DFIR, and red-team modules
carry explicit authorization gates (e.g. the capstone's live-detonation gate and
the offensive modules' lab-only banners). **Never weaken these gates.** Never put
real secrets in committed files — the secrets adapters deliberately redact, and
reports must not leak credentials.

## Working notes

- Don't truncate inputs to the model; if content is too large, chunk/summarize
  and say so — don't silently drop data.
- Prefer extending shared `aug`/`automation` over per-module reimplementation.
- The repo's default branch is `main`.
- The curriculum is built to make progress legible: a `project/` stub raising
  `NotImplementedError` means "not yet built", and `ROADMAP.md` is the checklist —
  useful when asked "what's missing / what's next".

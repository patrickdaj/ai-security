# Capstone — The AI Security Copilot

Tie the modules together into one tool: an agent that orchestrates the
deterministic security tooling you've toured and applies AI judgment across the
whole pipeline. This is where you go from "eleven scripts" to "a system."

## What you build

A copilot that, pointed at a target (a repo, an image, or a running app in your
lab), can:

1. **Run the right tools** — SAST (01), secrets (02), SBOM/CVEs (03), and a web
   scan (04) — orchestrated as tool calls.
2. **Normalize** everything into the shared `Finding` schema.
3. **Triage and correlate** — reuse the `aug` triage engine, then *correlate
   across tools* (a reachable CVE in code a SAST finding also touches is more
   urgent than either alone).
4. **Report** — produce a prioritized, human-readable report with fixes, gating
   anything destructive behind review.

## Architecture choice

This is a real "should I build an agent?" decision. Two valid shapes:

- **Workflow (recommended start):** you orchestrate the loop in code — run tool,
  normalize, call `aug` for judgment, next tool. Deterministic, debuggable, and
  enough for a fixed pipeline. Build this first.
- **Agentic / tool-use:** give Claude a set of tools (run_semgrep, run_grype,
  read_file, ...) and let it decide what to run next based on what it finds. More
  flexible, more surface area. Graduate to this once the workflow works.

Either way, the tools that *act* (run a scanner, write a file) are dedicated,
typed tool calls so your harness can gate, log, and parallelize them — and so a
destructive action (apply a fix, touch a live system) always passes through a
human gate.

## Build path

1. Wrap each module's scanner as a function returning `list[Finding]`.
2. Compose them into a workflow that triages and ranks.
3. Add cross-tool correlation: join findings by file/package/endpoint and let
   the model reason about combined risk.
4. Generate the final report (Markdown + JSON).
5. Stretch: convert the workflow into a tool-use agent and compare.

## Exercises / extensions

- Add the detection-engineering output (09): when the copilot finds an
  exploitable issue, also emit a Sigma/Suricata rule to detect exploitation.
- Add a "fix PR" mode that opens a branch with the high-confidence, low-risk
  remediations from modules 01 and 08 — review-gated, never to `main`.
- Run the copilot in CI against your lab app and fail the build on new
  high-confidence true positives.
- **Infra coverage:** extend the copilot to run the Infrastructure & Runtime
  modules — pull cloud IAM attack paths (11), audit the pipeline (12), triage
  runtime alerts (13), and check host hardening (14) — and correlate across
  layers (a reachable CVE in code with an over-permissioned role that exposes it
  is worse than either alone).
- **Purple-team loop (cloud attack emulation):** add Stratus Red Team / Pacu /
  Atomic Red Team. Have the copilot pick relevant ATT&CK TTPs for the
  environment, emulate them (authorized accounts only), check whether your
  detections (09) and runtime tooling (13) caught them, and — when they didn't —
  synthesize the missing Sigma/Falco rule. This closes the offense → detection
  loop across modules 09, 11, 13, and 15.

## Project starters

- [`project/purple_loop.py`](./project/purple_loop.py) — a working cloud
  purple-team loop: the model plans relevant Stratus Red Team techniques,
  detonation runs them (behind a hard authorization gate), the model judges
  whether your telemetry caught each one, and for gaps it synthesizes the
  missing Sigma rule. Runs safely in dry-run over a recorded events file:

  ```bash
  python modules/capstone/project/purple_loop.py \
      --env-desc env.txt \
      --events modules/capstone/project/sample_cloudtrail.json
  ```

  Live detonation (`--live`) is refused unless you also pass `--i-am-authorized`
  and set `STRATUS_ALLOW=1` — real attack techniques against a real account
  require explicit, multi-signal authorization. That gate is the point: the AI
  plans and writes detections; a human authorizes the irreversible step.

## Done when

- One command against your lab target produces a prioritized, cross-correlated,
  human-readable security report with concrete fixes — and you can defend every
  prioritization decision the copilot made by pointing at the evidence.

---

You now have a portfolio: eleven AI-augmented security tools and a copilot that
orchestrates them. The throughline — *tools find candidates, AI scales the
judgment, humans gate the irreversible* — is the thing to carry into real work.

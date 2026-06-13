# Module 21 — Security Operations & SIEM

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Defensive Operations.** Module 09 taught detection *authoring*; this is
the SOC seat where detections *run*: a SIEM full of logs, an alert queue, and a
clock. The two AI wins are turning intent into the platform's query language and
adding a judgment layer to alert triage so analysts stop drowning.

## Tools you tour

- **Splunk / Elastic Security / Microsoft Sentinel** — the SIEMs and their query
  languages (SPL / EQL / KQL). Pick one to go deep; the concepts transfer.
- **Sysmon** — rich Windows endpoint telemetry (the detection-engineer's lifeblood).
- **OCSF / ECS** — the schemas you normalize disparate logs into.
- **Shuffle / Tines / n8n** — open-source SOAR for response playbooks.

### Tour tasks

```bash
# Stand up Elastic + Kibana (or Splunk free) and ship Sysmon + auth logs in.
# Write the same detection three ways and feel the query-language tax:
#   Splunk SPL:  index=win EventCode=4688 NewProcessName="*\\powershell.exe" ...
#   Elastic EQL: process where process.name == "powershell.exe" and ...
#   Sentinel KQL: SecurityEvent | where EventID == 4688 | where ...
```

## AI augmentation: NL→query + an alert-triage copilot

Two builds (see [`project/`](./project), worked answer in [`reference/`](./reference)):

1. **Query generator.** Given a detection intent in plain language, emit the
   correct query for your backend (SPL/EQL/KQL) as a typed
   [`PolicyDraft`](../../aug/models.py) — render and validate it against sample logs.
2. **Alert triage copilot.** Normalize an alert + its surrounding events into a
   `Finding`, then triage it: true/false positive, severity in context, the
   enrichment that decided it, and the next SOAR action.

The point: the SIEM finds candidates; the copilot supplies the judgment that
turns a 10,000-alert day into a handful of real incidents — the same noise-kill
move as SAST triage, applied to operations.

## Exercises

1. Generate one detection in two backends from the same intent; confirm both
   fire on a malicious sample and stay quiet on benign telemetry.
2. Triage a labeled alert set and measure the copilot's FP/TP agreement with
   your own calls.
3. Wire a confirmed incident into a SOAR playbook (isolate host, open ticket).

## Done when

- You can turn intent into a validated SIEM detection on a real backend, and run
  a labeled alert queue through a triage copilot that measurably cuts the noise.

## SOAR with n8n (AI-routed playbook)

The triage copilot decides; a SOAR tool acts. Build the low-code version:

1. **Triage service** — [`project/triage_service.py`](./project/triage_service.py)
   (worked answer: [`reference/triage_service.py`](./reference/triage_service.py))
   is a tiny webhook that wraps the shared `aug` triage engine: POST an alert,
   get back a typed verdict. Any SOAR can call it.
2. **n8n workflow** — import [`reference/n8n/soar-triage.workflow.json`](./reference/n8n/soar-triage.workflow.json):
   an alert hits a webhook → the workflow calls the triage service → a Switch
   routes on `verdict` (true positive → notify + ticket; false positive →
   suppress; needs review → analyst queue). See
   [`example-output/soar-run.md`](./example-output/soar-run.md).

Same "AI is the judgment layer, humans gate the irreversible" pattern as the
Python pipeline (module 16) — but visual and analyst-readable. n8n's native LLM
nodes can also do the triage inline if you'd rather not run the service.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Splunk Search Reference (SPL)](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference)
- [Elastic Security / EQL](https://www.elastic.co/guide/en/security/current/index.html)
- [Microsoft Sentinel + KQL](https://learn.microsoft.com/en-us/azure/sentinel/)
- [Sysmon (Sysinternals)](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [OCSF schema](https://schema.ocsf.io/) · [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/index.html)
- [n8n docs](https://docs.n8n.io/) · [n8n AI / LangChain nodes](https://docs.n8n.io/advanced-ai/) · [Shuffle SOAR](https://shuffler.io/)

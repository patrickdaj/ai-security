# Module 23 — Threat Intelligence & Hunting

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Defensive Operations.** Detection waits for a known-bad to fire; hunting
goes looking for the unknown-bad on a hypothesis. Threat intel feeds both. The
bottlenecks — reading a flood of reports into structured indicators, and turning
TTPs into hunt hypotheses — are textbook AI extraction and synthesis.

## Tools you tour

- **MISP** — threat-intel sharing platform; IOC management and correlation.
- **OpenCTI** — knowledge graph of threats (actors, TTPs, infrastructure).
- **STIX / TAXII** — the structured-intel data model and transport.
- **Velociraptor** — endpoint hunting and live response at fleet scale.
- **Jupyter** — the hunter's notebook (query → pivot → visualize → conclude).

### Tour tasks

```bash
# Stand up MISP/OpenCTI (docker), import a feed, and explore the graph.
# In a notebook, pull telemetry (from module 21's SIEM) and pivot on an IOC.
```

## AI augmentation: report → structured intel + hunt-hypothesis generator

Build a tool that ingests a prose threat report and returns typed intel: a
summary, **structured indicators** (type/value/context), the **ATT&CK
techniques**, and a set of **hunt hypotheses** ("if this actor were here, we'd
see X in our telemetry — go look"). See [`project/`](./project) /
[`reference/`](./reference). This closes the loop with module 09 (intel →
detection) and the capstone purple loop (TTPs → emulation).

## Exercises

1. Extract IOCs + TTPs from a public APT report; push the IOCs into MISP and the
   techniques onto an ATT&CK Navigator layer.
2. Turn one technique into a hunt hypothesis and run it against module 21's
   telemetry in a notebook; document the finding (or the clean result).
3. Dedup/merge two overlapping reports into one actor profile with the model.

## Done when

- You can turn a prose report into structured, shareable intel and an executed
  hunt — and feed the result back into detection (09) and emulation (capstone).

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [MISP docs](https://www.misp-project.org/documentation/)
- [OpenCTI docs](https://docs.opencti.io/)
- [STIX/TAXII (OASIS)](https://oasis-open.github.io/cti-documentation/)
- [Velociraptor docs](https://docs.velociraptor.app/)
- [MITRE ATT&CK](https://attack.mitre.org/) · [ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator)
- [The PARIS Model / hunting methodology](https://www.threathunting.net/)

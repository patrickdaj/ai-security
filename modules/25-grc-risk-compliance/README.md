# Module 25 — GRC, Risk & Compliance

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Governance & end-to-end tie-off.** Every other module *produces*
security evidence; GRC *consumes* it — mapping findings to framework controls,
assessing gaps, quantifying risk, and writing the policies and evidence auditors
want. It's enormous, repetitive document work, which is the single best fit for
AI in this whole curriculum after detection.

## Tools you tour

- **Frameworks** — ISO 27001, SOC 2, PCI-DSS, NIST CSF / 800-53, FedRAMP.
- **Risk quantification** — FAIR (loss-event frequency × magnitude), risk registers.
- **OSCAL** — machine-readable controls and assessment results.
- **TPRM & privacy** — vendor questionnaires, GDPR/CCPA data mapping.

### Tour tasks

```bash
# Map this repo's existing findings (from any module's example-output) to a
# framework, then identify which controls have no evidence.
```

## AI augmentation: control mapper + gap assessment + policy/evidence generator

Build a tool that ingests findings/controls and a target framework and returns a
**compliance assessment**: each finding mapped to the control(s) it satisfies or
violates, the **gaps** (controls with no evidence), and a risk narrative. Extend
it to generate policy/standard text and to auto-collect evidence from the
pipeline's outputs. See [`project/`](./project) / [`reference/`](./reference).
This is where the whole curriculum's output becomes an audit story.

## Exercises

1. Map the findings from modules 01/03/08/11 to SOC 2 / ISO 27001 controls and
   produce a gap list.
2. Generate a policy (e.g. access control or logging) and check it against the
   relevant control's intent.
3. Quantify the risk of one top gap with a FAIR-style estimate (frequency ×
   magnitude) and write the risk-register entry.

## Done when

- You can turn the curriculum's security evidence into a framework-mapped gap
  assessment, generate policy/evidence, and express residual risk in business terms.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) · [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [ISO/IEC 27001](https://www.iso.org/standard/27001) · [SOC 2 (AICPA)](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)
- [PCI DSS](https://www.pcisecuritystandards.org/) · [FedRAMP](https://www.fedramp.gov/)
- [FAIR risk model (Open Group)](https://www.opengroup.org/forum/security-forum-0/openfair)
- [OSCAL](https://pages.nist.gov/OSCAL/)

# Module 17 — Security Architecture & Threat Modeling

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Architecture, Identity, Crypto, Network.** Every other module reacts to
a built system; this one shapes it *before* it's built. Threat modeling — find
the threats in a design, pick the controls — is the highest-leverage security
activity and the most tedious to do well at scale. Reading a design and
enumerating STRIDE threats is exactly what AI accelerates.

## Tools you tour

- **STRIDE / PASTA** — threat-classification and risk-centric methodologies.
- **Data Flow Diagrams + trust boundaries** — the substrate you threat-model over.
- **Attack trees** — decompose an attacker goal into paths.
- **OWASP Threat Dragon / pytm** — threat-modeling-as-code.

### Tour tasks

```bash
# Model a small system in pytm (threat-model-as-code) and generate the report.
pip install pytm && python tm.py --report template.md
```

## AI augmentation: design → threat model + control selection

Build a tool that ingests a design (a doc, a description, or a DFD) and returns a
typed **`ThreatModel`**: the assets and trust boundaries, the STRIDE threats per
data flow, and a recommended control for each — plus abuse cases. See
[`project/`](./project) / [`reference/`](./reference). It's a design-review
copilot: the model does the exhaustive enumeration; you make the risk calls.

## Exercises

1. Threat-model one of this repo's own components (the automation pipeline, the
   capstone copilot) and produce a control list.
2. Generate abuse cases for an auth flow and check them against the OWASP ASVS.
3. Turn the threat model into tracked work items (one per unmitigated threat).

## Done when

- You can take a system design and produce a defensible threat model — assets,
  trust boundaries, STRIDE threats, and selected controls — that a team can act on.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [pytm (threat-model-as-code)](https://github.com/OWASP/pytm) · [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST SP 800-160 (systems security engineering)](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)

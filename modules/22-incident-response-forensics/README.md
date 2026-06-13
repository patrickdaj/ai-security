# Module 22 — Incident Response & Digital Forensics (DFIR)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Defensive Operations.** Detection tells you *something happened*; IR is
what you do next — contain, investigate, forensicate, recover, and write it up.
The work is drowning in artifacts (memory, disk, logs, malware) and racing a
clock. Summarization and triage are exactly what AI accelerates.

> **Ethics/safety gate:** analyze malware and images **only** in an isolated VM
> with no network. Use public CTF/forensics images and *defanged* samples. Treat
> everything as live; never detonate on a host you care about.

## Tools you tour

- **Volatility 3** — memory forensics (processes, injection, network, hashes).
- **Autopsy / The Sleuth Kit** — disk forensics and artifact extraction.
- **plaso / log2timeline** — build a super-timeline across all artifacts.
- **YARA** — pattern-match malware/IOCs across files and memory.
- **CloudTrail / cloud audit logs** — the cloud equivalent of forensics.

### Tour tasks (isolated VM only)

```bash
vol -f memory.raw windows.pslist           # processes from a memory image
vol -f memory.raw windows.malfind          # injected code
log2timeline.py timeline.plaso disk.E01    # super-timeline
yara rules.yar suspicious.bin              # match known patterns
```

## AI augmentation: timeline + artifact summarizer, report drafter

Build a tool that ingests the noisy outputs above (a Volatility dump, a plaso
timeline slice, strings/imports of a sample) and returns a typed
**`IncidentSummary`**: what happened, ATT&CK techniques, a reconstructed
timeline, the likely root cause, and a containment recommendation — then drafts
the incident report and stakeholder comms. See [`project/`](./project) /
[`reference/`](./reference).

The judgment stays yours; the model does the reading and first-draft synthesis
across thousands of artifact rows so you investigate, not transcribe.

## Exercises

1. From a public memory image, have the model summarize the malicious process
   tree and injection, grounded in the Volatility output.
2. Slice a plaso timeline around the suspected compromise window and get a
   plain-language reconstruction with timestamps.
3. Triage a defanged sample from its strings/imports into a behavior summary +
   a YARA rule; draft the incident report.

## Done when

- You can take raw DFIR artifacts (memory, timeline, sample) and produce a
  defensible incident timeline, root cause, containment plan, and report — every
  claim traceable to an artifact.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Volatility 3 docs](https://volatility3.readthedocs.io/)
- [Autopsy / The Sleuth Kit](https://www.autopsy.com/)
- [plaso / log2timeline](https://plaso.readthedocs.io/)
- [YARA docs](https://yara.readthedocs.io/)
- [NIST SP 800-61 Computer Security Incident Handling Guide](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [SANS DFIR posters & cheat sheets](https://www.sans.org/posters/?focus-area=digital-forensics)

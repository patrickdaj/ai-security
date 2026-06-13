# Roadmap — closing every gap to full generalist coverage

This curriculum started AppSec/cloud/DevSecOps/detection-heavy. This roadmap
extends it to the **full security lifecycle** so a generalist can run it end to
end: **architect → build → ship → detect → respond → hunt → govern.**

Each new piece follows the same pattern as every other module: a `project/`
stub you build, a `reference/` worked solution, an `example-output/` target, a
README with an AI augmentation, Resources, a lab target, and the Codespaces
badge.

## Gap → module map

| Gap (role) | Was | Closed by |
|---|:--:|---|
| Incident Response / DFIR | 🔴 | M22 — IR & Digital Forensics |
| Red Team / Adversary Ops | 🔴 | M24 — Offensive Operations |
| Cryptography / Data Security | 🔴 | M20 — Cryptography & Data Security |
| Network Security | 🟠 | M18 — Network Security Engineering |
| Threat Hunting / Intel | 🟠 | M23 — Threat Intelligence & Hunting |
| GRC / Risk / Compliance | 🟠 | M25 — GRC, Risk & Compliance |
| SOC Analyst | 🟡 | M21 — Security Operations & SIEM |
| Security Architect | 🟡 | M17 — Security Architecture & Threat Modeling |
| Identity / IAM (enterprise) | 🟡 | M19 — Enterprise Identity & Access Governance |
| Web/App Pentester | 🟡 | M04 — Advanced Web & API Exploitation (extension) |
| Vuln Research / Exploit Dev | 🟡 | M06/07 — Exploit Development (extension) |
| Cloud Red Team (on-host) | 🟡 | folded into M24 |

## Progress board

Status: **Scaffolded** = README + stub + reference + example-output committed,
ready for you to build. **Done** = you've completed the `project/` and shipped
the deliverable.

### Phase 1 — Defensive Operations
- [ ] **M21 Security Operations & SIEM** — _Scaffolded_
- [ ] **M22 Incident Response & Digital Forensics** — _Scaffolded_
- [ ] **M23 Threat Intelligence & Hunting** — _Scaffolded_

### Phase 2 — Offensive Depth
- [ ] **M24 Offensive Operations (Red Team)** — _Scaffolded_
- [ ] **M04 Advanced Web & API Exploitation** (extends module 04) — _Scaffolded_
- [ ] **M06/07 Exploit Development** (extends modules 06/07) — _Scaffolded_

### Phase 3 — Architecture, Identity, Crypto, Network
- [ ] **M17 Security Architecture & Threat Modeling** — _Scaffolded_
- [ ] **M20 Cryptography & Data Security** — _Scaffolded_
- [ ] **M19 Enterprise Identity & Access Governance** — _Scaffolded_
- [ ] **M18 Network Security Engineering** — _Scaffolded_

### Phase 4 — Governance & end-to-end tie-off
- [ ] **M25 GRC, Risk & Compliance** — _Scaffolded_
- [ ] **Capstone v2** — copilot spans the full lifecycle — _Scaffolded_

## How to run it end to end

1. Pick the next module on the board.
2. Read its README and `example-output/` (the target).
3. Build its `project/` stub; check `reference/` when stuck.
4. Ship the deliverable; the capstone copilot consumes it.
5. Tick the box; move the role to 🟢 on the heatmap in the README.

## Definition of done (generalist-ready)

- No 🔴/🟠 roles left on the heatmap; every role 🟡+.
- A portfolio deliverable per module.
- A capstone copilot that runs the full lifecycle in one pass.

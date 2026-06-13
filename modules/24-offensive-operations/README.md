# Module 24 — Offensive Operations (Red Team)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Offensive Depth.** The earlier offensive modules find *vulnerabilities*;
this one is operating as an adversary through the **kill chain** — initial
access, Active Directory attack, privilege escalation, lateral movement, C2,
exfil. It's what makes the purple-team capstone credible from the red side and
what "red team" actually means on a job description.

> **Authorization gate — non-negotiable.** Everything here runs against a lab AD
> range you own (GOAD or a vagrant build) or a written, scoped engagement.
> Attacking systems without authorization is a crime. The AI augmentation
> reasons and reports; it does not lower this bar.

## Tools you tour

- **BloodHound / SharpHound** — graph AD attack paths to Domain Admin.
- **Impacket** — Kerberoasting, AS-REP roasting, NTLM relay, secretsdump.
- **NetExec (CrackMapExec)** — spray, enumerate, move laterally.
- **Sliver / Mythic** — open-source C2 frameworks (beacons, tasking, OPSEC).
- **hashcat** — crack the hashes you collect.

### Tour tasks (your lab AD only)

```bash
# Collect the graph, then ask BloodHound for the shortest path to DA.
SharpHound.exe -c All
# Kerberoast and crack
impacket-GetUserSPNs -request -dc-ip 10.0.0.10 lab.local/user
hashcat -m 13100 hashes.txt rockyou.txt
```

## AI augmentation: attack-path narrator + next-move advisor

Build a tool that takes the BloodHound path data (or your enum output) and
returns a typed [`AttackPath`](../../aug/models.py): the kill chain hop by hop,
the **next move** to take, and — because you're really doing purple — the
**single change that breaks the path** for the defenders. See
[`project/`](./project) / [`reference/`](./reference). The model reasons over the
graph the tools computed; it does not invent edges (same discipline as the CIEM
module 11). It also drafts the engagement report.

## Exercises

1. Walk a full path from a low-priv user to Domain Admin in your lab; have the
   model narrate each hop and propose the next technique.
2. For each hop, get the defensive fix and hand it to module 09/21 as a detection.
3. Run a Sliver beacon through the chain and document OPSEC choices (jitter,
   named pipes) and what telemetry they generate.

## Done when

- You can take a lab from a foothold to domain dominance, narrate the kill chain
  with the next move at each step, and produce both an engagement report and the
  detections that would have caught you.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [BloodHound docs](https://bloodhound.specterops.io/)
- [Impacket](https://github.com/fortra/impacket) · [NetExec](https://www.netexec.wiki/)
- [Sliver C2](https://sliver.sh/docs) · [Mythic C2](https://docs.mythic-c2.net/)
- [GOAD — Game of Active Directory lab](https://github.com/Orange-Cyberdefense/GOAD)
- [MITRE ATT&CK](https://attack.mitre.org/) · [The Hacker Recipes (AD)](https://www.thehacker.recipes/)

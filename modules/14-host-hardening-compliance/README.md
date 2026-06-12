# Module 14 — Host Hardening & Compliance-as-Code

Phase: **Infrastructure & Runtime.** Below the cloud and cluster layers are
actual hosts that drift from their hardened baseline and must answer to
compliance frameworks. Scanners tell you *which* control failed precisely;
turning that into applied remediation and mapping it to the right control is the
toil AI removes.

## Tools you tour

- **OpenSCAP** — SCAP-based compliance scanning against CIS/STIG profiles.
- **Lynis** — host hardening auditor; fast, readable findings.
- **Chef InSpec** — compliance-as-code; tests you can author and run.
- **dev-sec.io** — Ansible/Chef hardening baselines you can apply.
- **osquery** — query the host (and a fleet, via Fleet) like a database; great
  for drift detection and enrichment.

### Tour tasks

```bash
oscap xccdf eval --profile cis --results scratch/oscap.xml <ds.xml>
lynis audit system
osqueryi "select * from users where username = 'root';"
inspec exec <profile>
```

Read a Lynis/OpenSCAP finding. It names a control and a current value. The fix
lives in *your* config (sshd_config, sysctl, a systemd unit) and must map to a
framework control — both perfect for the model.

## AI augmentation: remediation-as-code + control mapper

Build a tool that ingests OpenSCAP/Lynis findings, reads the relevant host
config into `.context`, and returns a [`Remediation`](../../aug/models.py): an
Ansible task (or InSpec test + fix) that satisfies the control, a
breaking-change risk, and the `compliance_controls` it maps to (CIS / SOC2 /
PCI). Use the breaking-change risk as the gate: auto-apply benign hardening
(sysctl tightening), hold risky ones (disabling a service) for review.

A second build: drift detection. Snapshot osquery state, and when it diverges
from the hardened baseline, have the model explain the drift and propose the
re-hardening task.

## Exercises

1. Convert a batch of Lynis findings into idempotent Ansible tasks; apply the
   safe ones to a scratch VM and re-scan to confirm they clear.
2. Map a set of findings to CIS control IDs and generate the compliance
   evidence narrative.
3. Diff osquery snapshots across two points in time and have the model summarize
   the security-relevant drift.

## Done when

- You can take a host scan and produce review-ready Ansible/InSpec remediation
  that clears the findings on re-scan, each tagged with the compliance control
  it satisfies and a breaking-change risk.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [OpenSCAP](https://www.open-scap.org/)
- [Lynis](https://cisofy.com/documentation/lynis/)
- [Chef InSpec](https://docs.chef.io/inspec/)
- [dev-sec.io hardening](https://dev-sec.io/)
- [osquery](https://osquery.readthedocs.io/)
- [DISA STIGs](https://public.cyber.mil/stigs/)

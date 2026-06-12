"""STUB — host hardening remediation-as-code. Reference: ../reference/.

Turn Lynis/OpenSCAP findings into idempotent Ansible tasks, mapped to compliance
controls. The breaking-change risk gates auto-apply.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402


def from_lynis(warning: dict) -> Finding:
    # TODO: map a Lynis warning -> Finding (the control id, the host setting).
    raise NotImplementedError("Build the Lynis -> Finding adapter.")


def remediate(client: AugClient, f: Finding) -> Remediation:
    # TODO: prompt for an idempotent Ansible task that satisfies the control,
    # the breaking_change_risk, and compliance_controls (CIS/SOC2/PCI).
    # return client.reason(prompt, Remediation)
    raise NotImplementedError("Build the host-remediation prompt.")


if __name__ == "__main__":
    print("Load Lynis findings, remediate, apply low-risk only. See reference.")

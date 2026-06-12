"""STUB — IaC remediation-as-code. Reference: ../reference/.

Run Checkov/tfsec against ./terraform (the misconfigured target), read the
offending HCL into context, and generate a review-ready fix. The
breaking-change risk is the gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402


def from_checkov(check: dict) -> Finding:
    # TODO: map a checkov failed_check -> Finding, pulling the file + the
    # offending HCL block (check["code_block"]) into .context.
    raise NotImplementedError("Build the Checkov -> Finding adapter.")


def remediate(client: AugClient, finding: Finding) -> Remediation:
    # TODO: prompt for a minimal patch that satisfies the policy while preserving
    # surrounding config; ask for breaking_change_risk + compliance_controls.
    # return client.reason(prompt, Remediation)
    raise NotImplementedError("Build the remediation prompt.")


if __name__ == "__main__":
    print("Load checkov JSON, remediate, auto-apply low-risk only. See reference.")

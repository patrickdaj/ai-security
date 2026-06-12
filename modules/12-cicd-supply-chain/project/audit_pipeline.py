"""STUB — CI/CD pipeline auditor. Reference: ../reference/.

Run zizmor over .github/workflows/, normalize each finding (with the offending
workflow block in context), and generate a fix that explains the attack.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402


def from_zizmor(finding: dict) -> Finding:
    # TODO: map a zizmor finding -> Finding, pulling the workflow file + the
    # offending step/job block into .context.
    raise NotImplementedError("Build the zizmor -> Finding adapter.")


def audit(client: AugClient, finding: Finding) -> Remediation:
    # TODO: prompt for an explanation of the attack (e.g. pull_request_target +
    # checkout of PR head leaks secrets to fork code) and a patch that fixes it
    # without breaking the workflow. return client.reason(prompt, Remediation)
    raise NotImplementedError("Build the pipeline-audit prompt.")


if __name__ == "__main__":
    print("Run zizmor -> normalize -> audit. See the reference.")

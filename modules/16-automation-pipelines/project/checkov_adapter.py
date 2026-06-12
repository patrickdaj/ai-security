"""STARTER STUB — add Checkov (IaC scanning) to the pipeline.

Your task: finish `checkov` so it runs Checkov over a target and normalizes each
result into an `aug.Finding`, then register it so the pipeline picks it up:

    from automation.scanners import REGISTRY
    from checkov_adapter import checkov
    REGISTRY["checkov"] = checkov

Test it against the deliberately-misconfigured Terraform from module 08:

    python -c "from checkov_adapter import checkov; \
        [print(f.rule_id, f.location) for f in checkov('../../08-cloud-iac/project/terraform')]"

Follow the pattern in automation/scanners.py (the semgrep/trivy adapters). The
point of writing this yourself: you internalize the normalize step that makes
every tool's output one shape.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import Finding, Severity  # noqa: E402

# Checkov severities are not always present per-check; map what you find.
_SEV = {
    "LOW": Severity.low,
    "MEDIUM": Severity.medium,
    "HIGH": Severity.high,
    "CRITICAL": Severity.critical,
}


def checkov(target: str) -> list[Finding]:
    if not shutil.which("checkov"):
        return []

    proc = subprocess.run(
        ["checkov", "-d", target, "-o", "json", "--compact"],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []

    # checkov returns either a dict or a list of {check_type, results:{failed_checks}}.
    blocks = data if isinstance(data, list) else [data]
    findings: list[Finding] = []
    for block in blocks:
        for c in block.get("results", {}).get("failed_checks", []):
            # TODO: map a single failed check into a Finding. Pull:
            #   - c["check_id"]            -> rule_id
            #   - c["check_name"]          -> title
            #   - c["file_path"] + line    -> location
            #   - c["severity"]            -> severity (via _SEV, default medium)
            #   - the code_block snippet   -> context (great for triage!)
            # and append a Finding(tool="checkov", ...).
            raise NotImplementedError("Build the Checkov -> Finding mapping.")
    return findings

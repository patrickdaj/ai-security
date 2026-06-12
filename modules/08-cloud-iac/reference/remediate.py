"""REFERENCE — IaC remediation-as-code (worked answer).

    checkov -d ../project/terraform -o json > scratch/checkov.json
    python remediate.py scratch/checkov.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402


def from_checkov(check: dict) -> Finding:
    block = "\n".join(line for _, line in check.get("code_block", []))
    return Finding(
        tool="checkov",
        rule_id=check.get("check_id", "?"),
        title=check.get("check_name", "")[:120],
        severity=Severity.medium,
        location=f"{check.get('file_path', '?')}:{(check.get('file_line_range') or [0])[0]}",
        description=check.get("check_name", ""),
        context=block,
        raw={"id": check.get("check_id")},
    )


_PROMPT = """A Terraform misconfiguration was flagged. Produce a minimal patch
that satisfies the policy while preserving the surrounding config and style,
as a unified diff. Rate breaking_change_risk (a tag/encryption change is low; an
IAM or networking change is high) and list the compliance_controls it satisfies.

Check: {rule} — {title}
File: {loc}
Offending HCL:
```hcl
{ctx}
```"""


def remediate(client: AugClient, f: Finding) -> Remediation:
    prompt = _PROMPT.format(rule=f.rule_id, title=f.title, loc=f.location, ctx=f.context)
    return client.reason(prompt, Remediation)


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    checks = (data.get("results", {}) if isinstance(data, dict) else {}).get("failed_checks", [])
    client = AugClient()
    for c in checks:
        f = from_checkov(c)
        r = remediate(client, f)
        gate = "AUTO-APPLY" if r.breaking_change_risk.value in ("info", "low") else "REVIEW"
        print(f"[{gate}] {f.rule_id} @ {f.location} (risk {r.breaking_change_risk.value})")
        print(r.patch)


if __name__ == "__main__":
    main()

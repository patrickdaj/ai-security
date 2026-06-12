"""REFERENCE — host hardening remediation-as-code (worked answer)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402


def from_lynis(w: dict) -> Finding:
    return Finding(
        tool="lynis",
        rule_id=w.get("control", "?"),
        title=w.get("text", "")[:120],
        severity=Severity.medium,
        location=w.get("control", "?"),
        description=w.get("text", ""),
        context=w.get("details", ""),
        raw=w,
    )


_PROMPT = """A host-hardening scanner flagged a control. Produce an IDEMPOTENT
Ansible task (a YAML `- name:` block) that satisfies it, the breaking_change_risk
(a sysctl tweak is low; disabling a running service is high), and the
compliance_controls it maps to (CIS / SOC2 / PCI).

Control: {rule} — {title}
Detail: {ctx}"""


def remediate(client: AugClient, f: Finding) -> Remediation:
    prompt = _PROMPT.format(rule=f.rule_id, title=f.title, ctx=f.context or "(none)")
    return client.reason(prompt, Remediation)


def main() -> None:
    warnings = json.loads(Path(sys.argv[1]).read_text())
    client = AugClient()
    for w in warnings:
        f = from_lynis(w)
        r = remediate(client, f)
        gate = "AUTO" if r.breaking_change_risk.value in ("info", "low") else "REVIEW"
        print(f"[{gate}] {f.rule_id} controls={','.join(r.compliance_controls)}")
        print(r.patch)


if __name__ == "__main__":
    main()

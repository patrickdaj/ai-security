"""REFERENCE — CI/CD pipeline auditor (worked answer)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Remediation, Severity  # noqa: E402

_SEV = {"low": Severity.low, "medium": Severity.medium, "high": Severity.high}


def from_zizmor(f: dict) -> Finding:
    loc = (f.get("locations") or [{}])[0]
    path = loc.get("symbolic", {}).get("key", {}).get("Local", {}).get("given_path", "?")
    return Finding(
        tool="zizmor",
        rule_id=f.get("ident", "?"),
        title=f.get("desc", "")[:120],
        severity=_SEV.get(f.get("determinations", {}).get("severity", "medium").lower(),
                          Severity.medium),
        location=str(path),
        description=f.get("desc", ""),
        context=json.dumps(loc.get("concrete", {}), indent=2)[:1500],
        raw={"ident": f.get("ident")},
    )


_PROMPT = """A GitHub Actions workflow has a security finding. Explain the attack
concretely (who can exploit it and how — e.g. a fork PR exfiltrating secrets via
pull_request_target + checkout of the PR head), then give a patch that fixes it
without breaking the workflow. Rate breaking_change_risk.

Finding: {rule} — {title}
File: {loc}
Context:
```json
{ctx}
```"""


def audit(client: AugClient, f: Finding) -> Remediation:
    prompt = _PROMPT.format(rule=f.rule_id, title=f.title, loc=f.location, ctx=f.context)
    return client.reason(prompt, Remediation)


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    findings = data if isinstance(data, list) else data.get("findings", [])
    client = AugClient()
    for raw in findings:
        f = from_zizmor(raw)
        r = audit(client, f)
        print(f"[{f.rule_id}] {f.location} (risk {r.breaking_change_risk.value})")
        print(r.explanation)
        print(r.patch)


if __name__ == "__main__":
    main()

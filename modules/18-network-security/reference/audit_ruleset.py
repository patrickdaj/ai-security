"""REFERENCE — firewall ruleset auditor (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class RuleIssue(BaseModel):
    rule: str
    issue: str = Field(description="overexposed | dead | shadowed | too_broad")
    severity: Severity
    recommendation: str


class RulesetAudit(BaseModel):
    summary: str
    issues: list[RuleIssue]


_PROMPT = """Audit this firewall ruleset (nftables/iptables/cloud security group).
Reason over the rules as given. Flag: OVEREXPOSED rules (0.0.0.0/0 or ::/0 to
sensitive ports like 22/3389/5432/6379), DEAD/SHADOWED rules (unreachable because
an earlier rule already matches, or referencing nothing), and TOO-BROAD ranges or
port spans. For each, name the rule, the issue, severity, and a tightened
replacement.

Ruleset:
```
{ruleset}
```"""


def audit(client: AugClient, ruleset: str) -> RulesetAudit:
    return client.reason(_PROMPT.format(ruleset=ruleset[:10000]), RulesetAudit, max_tokens=10000)


def main() -> None:
    ruleset = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
    a = audit(AugClient(), ruleset)
    print(a.summary, "\n")
    for i in a.issues:
        print(f"[{i.severity.value}] {i.issue}: {i.rule}\n  -> {i.recommendation}")


if __name__ == "__main__":
    main()

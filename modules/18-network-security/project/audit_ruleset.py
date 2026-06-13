"""STUB — firewall ruleset auditor. Reference: ../reference/.

Find overexposed rules, dead/shadowed rules, and overly-broad ranges.
"""

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


def audit(client: AugClient, ruleset: str) -> RulesetAudit:
    # TODO: prompt the model over the ruleset (nft/iptables/security-group export)
    # for overexposed rules (0.0.0.0/0 on sensitive ports), dead/shadowed rules,
    # and too-broad ranges, each with a fix. return client.reason(prompt, RulesetAudit)
    raise NotImplementedError("Build the ruleset-audit prompt.")


if __name__ == "__main__":
    print("Feed an nft/iptables/security-group dump. See the reference.")

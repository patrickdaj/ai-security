"""REFERENCE — entitlement export -> access review (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class AccessFinding(BaseModel):
    principal: str
    issue: str = Field(description="over_grant | toxic_combination | stale | misconfig")
    detail: str
    severity: Severity
    recommendation: str


class AccessReview(BaseModel):
    findings: list[AccessFinding]


_PROMPT = """You are running an access review over this entitlement export
(principals and the roles/groups/permissions they hold, plus job titles and
last-login if present). Reason ONLY over the data given. Surface: over-grants
(access beyond the job function), toxic combinations (segregation-of-duties
violations — e.g. create AND approve payments, or dev AND prod-deploy), and stale
or dormant access. Give each a severity and a concrete recommendation.

Entitlements:
```
{ent}
```"""


def review(client: AugClient, entitlements: str) -> AccessReview:
    return client.reason(_PROMPT.format(ent=entitlements[:12000]), AccessReview, max_tokens=12000)


def main() -> None:
    ent = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
    r = review(AugClient(), ent)
    for f in r.findings:
        print(f"[{f.severity.value}] {f.issue}: {f.principal}\n  {f.detail}\n  -> {f.recommendation}")


if __name__ == "__main__":
    main()

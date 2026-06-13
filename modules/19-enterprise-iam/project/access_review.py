"""STUB — entitlement export -> access review. Reference: ../reference/.

Surface over-grants, toxic (SoD) combinations, and stale access.
"""

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


def review(client: AugClient, entitlements: str) -> AccessReview:
    # TODO: prompt the model over the entitlement export for over-grants vs. job
    # function, segregation-of-duties violations, and stale access — each with a
    # recommendation. return client.reason(prompt, AccessReview)
    raise NotImplementedError("Build the access-review prompt.")


if __name__ == "__main__":
    print("Feed an entitlement export. See the reference.")

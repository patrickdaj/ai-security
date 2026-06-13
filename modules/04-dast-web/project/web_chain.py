"""STUB (advanced track) — reason about chaining web/API vulns. Reference: ../reference/.

Authorized targets only (your lab). Scanners find single issues; the win is
chaining them (IDOR + SSRF + weak auth) into real impact, and reasoning about
access-control/auth flows tools miss.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class VulnChain(BaseModel):
    title: str
    steps: list[str] = Field(description="Ordered requests that compose the exploit")
    impact: str
    combined_severity: Severity


def analyze(client: AugClient, findings_and_traffic: str) -> VulnChain:
    # TODO: prompt the model over the individual findings + request/response
    # traffic to construct a multi-step exploit chain and rate combined impact.
    # return client.reason(prompt, VulnChain)
    raise NotImplementedError("Build the vuln-chaining prompt.")


if __name__ == "__main__":
    print("Feed findings + traffic from your authorized test. See the reference.")

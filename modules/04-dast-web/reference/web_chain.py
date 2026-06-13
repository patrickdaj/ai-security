"""REFERENCE (advanced track) — chain web/API vulns into real impact."""

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


_PROMPT = """You are assisting an AUTHORIZED web/API assessment. Below are
individual findings and request/response traffic. Reason about how they COMPOSE:
construct the most impactful multi-step exploit chain (e.g. an IDOR that leaks an
ID, feeding an SSRF, reaching an internal admin API), as an ordered list of
requests. Account for auth/session flow and access-control gaps the scanners
can't reason about. Rate the combined severity.

Findings + traffic:
```
{ctx}
```"""


def analyze(client: AugClient, findings_and_traffic: str) -> VulnChain:
    return client.reason(_PROMPT.format(ctx=findings_and_traffic[:10000]), VulnChain)


def main() -> None:
    ctx = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
    c = analyze(AugClient(), ctx)
    print(f"[{c.combined_severity.value}] {c.title}")
    for i, s in enumerate(c.steps, 1):
        print(f"  {i}. {s}")
    print(f"\nImpact: {c.impact}")


if __name__ == "__main__":
    main()

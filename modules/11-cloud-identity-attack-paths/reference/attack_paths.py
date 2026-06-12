"""REFERENCE — rank & explain cloud IAM attack paths (worked answer).

Feed candidate paths your tooling computed (PMapper privesc, Cartography Cypher).
The model prioritizes and explains; it does not invent edges.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AttackPath, AugClient  # noqa: E402


class PathList(BaseModel):
    paths: list[AttackPath]


_PROMPT = """These are candidate privilege-escalation / lateral-movement paths a
graph tool computed over a cloud account's IAM. Do NOT invent edges. Return the
most important paths as structured AttackPaths: entrypoint, target, each hop
(principal + the permission enabling the next hop), severity, calibrated
confidence, a plain-language narrative, and the single minimal policy change
that breaks each path. Rank by severity x confidence.

Candidate path data:
```json
{paths}
```"""


def rank(client: AugClient, candidates: dict) -> list[AttackPath]:
    prompt = _PROMPT.format(paths=json.dumps(candidates, indent=2)[:12000])
    return client.reason(prompt, PathList).paths


def main() -> None:
    candidates = json.loads(Path(sys.argv[1]).read_text())
    for p in rank(AugClient(), candidates):
        print(f"\n[{p.severity.value} {p.confidence:.2f}] {p.entrypoint} -> {p.target}")
        for i, s in enumerate(p.steps, 1):
            print(f"  {i}. {s.principal} --({s.action})-->")
        print(f"  {p.narrative}")
        if p.least_privilege_fix:
            print(f"  fix: {p.least_privilege_fix}")


if __name__ == "__main__":
    main()

"""Rank and explain cloud IAM attack paths with Claude.

Usage:
    python attack_paths.py pmapper_privesc.json

This is a starter. Feed it candidate paths your tooling already computed
(PMapper privesc output, or edges from a Cartography Cypher query) and it asks
the model to prioritize, explain, and propose the minimal fix. The model reasons
over the path data — it does not invent edges. See the module README.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AttackPath, AugClient  # noqa: E402

_PROMPT = """You are given candidate privilege-escalation / lateral-movement \
paths that graph tooling computed over a cloud account's IAM. Do NOT invent \
edges — reason only over what is given.

For the most important path below, return it as a structured AttackPath: the \
entrypoint, the target, each hop (principal + the permission that enables the \
next hop), a severity and calibrated confidence, a plain-language narrative an \
analyst can act on, and the single minimal policy change that breaks the path.

Candidate path data:
```json
{paths}
```"""


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: attack_paths.py <pmapper_or_cartography_paths.json>")
    paths = json.loads(Path(sys.argv[1]).read_text())

    client = AugClient()
    # TODO: iterate per candidate path / cluster, and dedup. For the starter we
    # hand the model the whole blob and ask for the top path.
    result: AttackPath = client.reason(
        _PROMPT.format(paths=json.dumps(paths, indent=2)[:12000]),
        AttackPath,
    )
    print(f"{result.entrypoint} -> {result.target}  "
          f"[{result.severity.value}, conf {result.confidence:.2f}]")
    for i, step in enumerate(result.steps, 1):
        print(f"  {i}. {step.principal}  --({step.action})-->")
    print(f"\n{result.narrative}")
    if result.least_privilege_fix:
        print(f"\nFix: {result.least_privilege_fix}")


if __name__ == "__main__":
    main()

"""REFERENCE — narrate an AD kill chain + next move (worked answer).

Authorized lab only. Reasons over the path the tools computed; invents nothing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AttackPath, AugClient  # noqa: E402

_PROMPT = """You are assisting an AUTHORIZED red-team engagement against a lab AD
range. Below is attack-path data a tool (BloodHound / enumeration) computed. Do
NOT invent edges. Return a structured AttackPath: entrypoint -> target (Domain
Admin or the goal), each hop as a principal plus the technique that enables the
next hop (e.g. Kerberoasting, DCSync, GenericAll abuse), a severity and
confidence, a narrative that includes the NEXT MOVE to take, and in
`least_privilege_fix` the single change that breaks the path for defenders.

Path data:
```json
{path}
```"""


def narrate(client: AugClient, path_data: dict) -> AttackPath:
    return client.reason(_PROMPT.format(path=json.dumps(path_data, indent=2)[:10000]),
                         AttackPath)


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
    p = narrate(AugClient(), data)
    print(f"{p.entrypoint} -> {p.target}  [{p.severity.value}, {p.confidence:.2f}]")
    for i, s in enumerate(p.steps, 1):
        print(f"  {i}. {s.principal} --({s.action})-->")
    print(f"\n{p.narrative}\n\nBlue-team fix: {p.least_privilege_fix}")


if __name__ == "__main__":
    main()

"""STUB — narrate an AD kill chain + next move. Reference: ../reference/.

Authorized lab only. Feed BloodHound path data / enum output; the model reasons
over what the tools found — it does not invent edges.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AttackPath, AugClient  # noqa: E402


def narrate(client: AugClient, path_data: dict) -> AttackPath:
    # TODO: prompt the model to turn the BloodHound/enumeration path into a typed
    # AttackPath: each hop (principal + the technique enabling the next), the next
    # move, and the single change that BREAKS the path for defenders.
    # return client.reason(prompt, AttackPath)
    raise NotImplementedError("Build the kill-chain narration prompt.")


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
    print(narrate(AugClient(), data).narrative)

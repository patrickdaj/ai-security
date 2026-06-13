"""STUB — intent -> SIEM detection query. Reference: ../reference/.

Generate the query for your backend, then validate it against sample logs.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402


def generate(client: AugClient, intent: str, backend: str = "spl") -> PolicyDraft:
    # TODO: prompt the model for a detection query in `backend` (spl|eql|kql)
    # from the intent — precise, low false-positive. Put the query in
    # PolicyDraft.policy, language=backend. return client.reason(prompt, PolicyDraft)
    raise NotImplementedError("Build the NL -> SIEM query prompt.")


if __name__ == "__main__":
    print(generate(AugClient(), "PowerShell spawned by Office with an encoded command").policy)

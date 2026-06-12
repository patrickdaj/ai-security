"""STUB — classify Gitleaks/TruffleHog hits. Reference: ../reference/.

Build the classifier: for each hit decide live / test / rotated / false-positive
and a blast radius. NEVER send a real secret to the model — classify on path +
surrounding context only.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class SecretVerdict(BaseModel):
    kind: str = Field(description="live | test_or_example | already_rotated | false_positive")
    is_live_guess: bool
    blast_radius: Severity
    rotate_now: bool
    rationale: str


def classify(client: AugClient, hit: dict) -> SecretVerdict:
    # TODO: build a prompt from the hit's file path, rule, and surrounding lines
    # (NOT the secret value). Weight the prior by path (tests/, examples/, *.md
    # lower the live probability). Then: return client.reason(prompt, SecretVerdict)
    raise NotImplementedError("Build the secret-classification prompt.")


if __name__ == "__main__":
    print("Load a gitleaks report and classify each hit. See the reference.")

"""STUB — prompt-injection red-team + scorer. Reference: ../reference/.

Dual-use, authorized targets only (your own app). Keep the attacker and the
scorer as SEPARATE model calls so the scorer isn't biased.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient  # noqa: E402


class InjectionAttempt(BaseModel):
    payload: str
    technique: str = Field(description="e.g. prompt-leak, role-override, tool-abuse")


class AttackResult(BaseModel):
    succeeded: bool
    evidence: str


def generate_attacks(client: AugClient, system_desc: str, n: int) -> list[InjectionAttempt]:
    # TODO: prompt the model to produce n injection payloads targeting system_desc.
    raise NotImplementedError("Build the attack-generation step.")


def score(client: AugClient, attempt: InjectionAttempt, app_response: str) -> AttackResult:
    # TODO: a SEPARATE call that judges whether app_response shows the injection
    # worked. return client.reason(prompt, AttackResult)
    raise NotImplementedError("Build the scorer (separate model call).")


if __name__ == "__main__":
    print("Generate -> run against YOUR app -> score. See the reference.")

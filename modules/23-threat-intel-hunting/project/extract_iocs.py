"""STUB — threat report -> structured intel + hunt hypotheses. Reference: ../reference/.

Turn prose into IOCs, ATT&CK techniques, and things to go look for.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient  # noqa: E402


class Indicator(BaseModel):
    type: str = Field(description="ip | domain | url | hash | email | ...")
    value: str
    context: str


class IntelExtract(BaseModel):
    summary: str
    indicators: list[Indicator]
    techniques: list[str] = Field(description="MITRE ATT&CK technique ids")
    hunt_hypotheses: list[str] = Field(description="If the actor is here, we'd see ...")


def extract(client: AugClient, report: str) -> IntelExtract:
    # TODO: prompt for structured indicators, ATT&CK techniques, and concrete
    # hunt hypotheses tied to telemetry. return client.reason(prompt, IntelExtract)
    raise NotImplementedError("Build the report -> intel extraction prompt.")


if __name__ == "__main__":
    print("Feed a threat report. See the reference.")

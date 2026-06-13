"""STUB — design -> STRIDE threat model. Reference: ../reference/.

Feed a system design (prose or a DFD); get assets, threats, and controls.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class Threat(BaseModel):
    stride: str = Field(description="Spoofing|Tampering|Repudiation|Info disclosure|DoS|EoP")
    where: str = Field(description="The data flow / component it applies to")
    description: str
    severity: Severity
    control: str = Field(description="The recommended mitigation")


class ThreatModel(BaseModel):
    assets: list[str]
    trust_boundaries: list[str]
    threats: list[Threat]


def model(client: AugClient, design: str) -> ThreatModel:
    # TODO: prompt the model to identify assets + trust boundaries, then enumerate
    # STRIDE threats per data flow with a recommended control each.
    # return client.reason(prompt, ThreatModel)
    raise NotImplementedError("Build the design -> threat-model prompt.")


if __name__ == "__main__":
    print("Feed a design doc/description. See the reference.")

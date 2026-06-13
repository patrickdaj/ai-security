"""STUB — findings -> framework gap assessment. Reference: ../reference/.

Map evidence to controls, find the gaps, narrate the risk.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class ControlMapping(BaseModel):
    finding: str
    control_ids: list[str] = Field(description="e.g. ['SOC2-CC6.1', 'ISO-A.9.2']")
    status: str = Field(description="satisfied | violated | no_evidence")
    note: str


class ComplianceAssessment(BaseModel):
    summary: str
    mappings: list[ControlMapping]
    top_gaps: list[str]


def assess(client: AugClient, findings: str, framework: str) -> ComplianceAssessment:
    # TODO: prompt the model to map each finding to controls in `framework`,
    # mark status, and surface the top gaps (controls with no evidence).
    # return client.reason(prompt, ComplianceAssessment)
    raise NotImplementedError("Build the control-mapping prompt.")


if __name__ == "__main__":
    print("Feed findings + a target framework. See the reference.")

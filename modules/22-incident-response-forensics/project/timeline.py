"""STUB — DFIR artifact summarizer. Reference: ../reference/.

Ingest noisy forensic output (Volatility, plaso, strings) and produce a typed
incident summary. Ground every claim in the artifacts.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class TimelineEvent(BaseModel):
    when: str
    what: str


class IncidentSummary(BaseModel):
    summary: str
    severity: Severity
    attack_techniques: list[str] = Field(description="MITRE ATT&CK technique ids")
    timeline: list[TimelineEvent]
    root_cause: str
    containment: str


def analyze(client: AugClient, artifacts: str) -> IncidentSummary:
    # TODO: prompt the model over the forensic artifacts for an IncidentSummary —
    # grounded in the rows, with ATT&CK mapping and a containment step.
    # return client.reason(prompt, IncidentSummary)
    raise NotImplementedError("Build the DFIR summarization prompt.")


if __name__ == "__main__":
    print("Feed Volatility/plaso/strings output. See the reference.")

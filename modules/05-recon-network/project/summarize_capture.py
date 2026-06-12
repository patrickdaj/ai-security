"""STUB — summarize a Zeek capture + draft a Suricata rule. Reference: ../reference/.

Zeek logs are already normalized rows; your job is to turn them into a
"what stands out" summary and a precise detection.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft, Severity  # noqa: E402


class CaptureSummary(BaseModel):
    narrative: str
    top_talkers: list[str]
    suspicious: list[str] = Field(description="Rare/long connections, odd DNS, etc.")


def summarize(client: AugClient, conn_log: str) -> CaptureSummary:
    # TODO: prompt the model over the Zeek rows for top talkers + a
    # plain-language "what stands out". return client.reason(prompt, CaptureSummary)
    raise NotImplementedError("Build the capture-summary prompt.")


def draft_rule(client: AugClient, behavior: str) -> PolicyDraft:
    # TODO: generate a Suricata rule (language='suricata') for the described
    # behavior; keep it precise. return client.reason(prompt, PolicyDraft)
    raise NotImplementedError("Build the Suricata-rule prompt.")


if __name__ == "__main__":
    print("Feed Zeek conn.log; see the reference.")

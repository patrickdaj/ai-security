"""REFERENCE — threat report -> structured intel + hunt hypotheses (worked answer)."""

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


_PROMPT = """Extract structured threat intelligence from this report. Pull every
indicator (type, value, and why it matters), map described behavior to MITRE
ATT&CK technique ids, and write concrete HUNT HYPOTHESES — each phrased as a
testable statement about what we'd find in our own telemetry if this actor were
present (e.g. "scheduled tasks named X on workstations"). Don't invent IOCs not
in the report.

Report:
{report}"""


def extract(client: AugClient, report: str) -> IntelExtract:
    return client.reason(_PROMPT.format(report=report[:12000]), IntelExtract, max_tokens=10000)


def main() -> None:
    report = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    x = extract(AugClient(), report)
    print(x.summary, "\n")
    for i in x.indicators:
        print(f"  IOC {i.type}: {i.value}  ({i.context})")
    print("\nTechniques:", ", ".join(x.techniques))
    print("\nHunts:")
    for h in x.hunt_hypotheses:
        print(f"  - {h}")


if __name__ == "__main__":
    main()

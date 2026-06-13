"""REFERENCE — DFIR artifact summarizer (worked answer)."""

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


_PROMPT = """You are assisting an incident responder. Below are forensic
artifacts (Volatility output, a plaso timeline slice, and/or strings/imports of a
sample). Reconstruct what happened: summarize the incident, map observed
behavior to MITRE ATT&CK techniques, build a timeline (timestamp + event) from
the artifacts ONLY, state the likely root cause, and recommend containment.
Ground every claim in a specific artifact; if the evidence is thin, say so.

Artifacts:
```
{artifacts}
```"""


def analyze(client: AugClient, artifacts: str) -> IncidentSummary:
    return client.reason(_PROMPT.format(artifacts=artifacts[:12000]), IncidentSummary,
                         max_tokens=12000)


def main() -> None:
    artifacts = Path(sys.argv[1]).read_text(errors="replace") if len(sys.argv) > 1 else ""
    s = analyze(AugClient(), artifacts)
    print(f"[{s.severity.value}] {s.summary}\nATT&CK: {', '.join(s.attack_techniques)}\n")
    for e in s.timeline:
        print(f"  {e.when}  {e.what}")
    print(f"\nRoot cause: {s.root_cause}\nContainment: {s.containment}")


if __name__ == "__main__":
    main()

"""REFERENCE — findings -> framework gap assessment (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient  # noqa: E402


class ControlMapping(BaseModel):
    finding: str
    control_ids: list[str] = Field(description="e.g. ['SOC2-CC6.1', 'ISO-A.9.2']")
    status: str = Field(description="satisfied | violated | no_evidence")
    note: str


class ComplianceAssessment(BaseModel):
    summary: str
    mappings: list[ControlMapping]
    top_gaps: list[str]


_PROMPT = """Map this security evidence to the {framework} control set. For each
finding/control, give the relevant control id(s), whether it is satisfied,
violated, or has no_evidence, and a short note. Then surface the TOP GAPS —
controls the evidence does not cover at all — as a prioritized list. Use real
control identifiers for {framework}.

Evidence/findings:
```
{findings}
```"""


def assess(client: AugClient, findings: str, framework: str) -> ComplianceAssessment:
    prompt = _PROMPT.format(framework=framework, findings=findings[:10000])
    return client.reason(prompt, ComplianceAssessment, max_tokens=12000)


def main() -> None:
    framework = sys.argv[1] if len(sys.argv) > 1 else "SOC 2"
    findings = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else sys.stdin.read()
    a = assess(AugClient(), findings, framework)
    print(a.summary, "\n")
    for m in a.mappings:
        print(f"[{m.status}] {', '.join(m.control_ids)} — {m.finding}")
    print("\nTop gaps:")
    for g in a.top_gaps:
        print(f"  - {g}")


if __name__ == "__main__":
    main()

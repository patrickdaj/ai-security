"""REFERENCE — design -> STRIDE threat model (worked answer)."""

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


_PROMPT = """Threat-model this system design. First identify the assets worth
protecting and the trust boundaries (where data crosses from less- to
more-trusted, or untrusted input enters). Then, for each significant data flow,
enumerate STRIDE threats (Spoofing, Tampering, Repudiation, Information
disclosure, Denial of service, Elevation of privilege), rate severity, and
recommend a concrete control for each. Be specific to THIS design, not generic.

Design:
{design}"""


def model(client: AugClient, design: str) -> ThreatModel:
    return client.reason(_PROMPT.format(design=design[:12000]), ThreatModel, max_tokens=14000)


def main() -> None:
    design = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    tm = model(AugClient(), design)
    print("Assets:", ", ".join(tm.assets))
    print("Trust boundaries:", ", ".join(tm.trust_boundaries), "\n")
    for t in tm.threats:
        print(f"[{t.severity.value}] {t.stride} @ {t.where}\n  {t.description}\n  control: {t.control}")


if __name__ == "__main__":
    main()

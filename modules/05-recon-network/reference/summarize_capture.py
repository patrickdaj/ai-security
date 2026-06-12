"""REFERENCE — Zeek capture summary + Suricata rule draft (worked answer).

Validate generated rules with `suricata -T -S generated.rules`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402


class CaptureSummary(BaseModel):
    narrative: str
    top_talkers: list[str]
    suspicious: list[str] = Field(description="Rare/long connections, odd DNS, etc.")


def summarize(client: AugClient, conn_log: str) -> CaptureSummary:
    prompt = (
        "These are Zeek conn.log rows (ts, src, dst, port, proto, duration, bytes). "
        "Identify the top talkers and call out what stands out — rare or long-lived "
        "connections, beaconing intervals, egress to odd destinations — grounded in "
        "the rows.\n\n" + conn_log[:8000]
    )
    return client.reason(prompt, CaptureSummary)


def draft_rule(client: AugClient, behavior: str) -> PolicyDraft:
    prompt = (
        f"Write a precise Suricata rule (language='suricata') matching this "
        f"behavior, tight enough to avoid firing on benign traffic: {behavior}. "
        f"Put the rule text in PolicyDraft.policy and give a should-match and a "
        f"should-not-match test case."
    )
    return client.reason(prompt, PolicyDraft)


def main() -> None:
    conn = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
    s = summarize(AugClient(), conn)
    print(s.narrative)
    print("Top talkers:", ", ".join(s.top_talkers))
    for x in s.suspicious:
        print(" suspicious:", x)


if __name__ == "__main__":
    main()

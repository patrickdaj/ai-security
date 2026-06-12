"""REFERENCE — your first adapter (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402


def load(record: dict) -> Finding:
    return Finding(
        tool="manual",
        rule_id=record.get("id", "?"),
        title=record.get("evidence", "")[:120],
        severity=Severity(record.get("severity", "medium")),
        location=record.get("where", "?"),
        description=record.get("evidence", ""),
        context=record.get("evidence", ""),
        raw=record,
    )


def main() -> None:
    rec = {"id": "DEMO-1", "where": "app.py:10", "evidence": "eval(user_input)",
           "severity": "high"}
    print(triage_finding(AugClient(), load(rec)).model_dump())


if __name__ == "__main__":
    main()

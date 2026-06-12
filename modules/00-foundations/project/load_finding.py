"""STUB — your first adapter. Reference: ../reference/.

Warm-up exercise: load a hand-written finding from JSON into the shared
`Finding` schema and triage it. Every later module writes an adapter like this.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding  # noqa: E402
from aug.triage import triage_finding  # noqa: E402


def load(record: dict) -> Finding:
    # TODO: map a plain dict (your own JSON shape) into a Finding. Decide which
    # keys become tool/rule_id/title/severity/location, and put the relevant
    # code/evidence into `context`.
    raise NotImplementedError("Map the dict into a Finding.")


if __name__ == "__main__":
    rec = {"id": "DEMO-1", "where": "app.py:10", "evidence": "eval(user_input)"}
    print(triage_finding(AugClient(), load(rec)))

"""STUB — crash triage / dedup / root-cause. Reference: ../reference/.

The clever bit is `dedup_key`: derive it from the crashing call site so
byte-different inputs that hit the same bug collapse to one.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class CrashAnalysis(BaseModel):
    bug_class: str = Field(description="e.g. heap-overflow, null-deref, IndexError")
    dedup_key: str = Field(description="Stable key from the root cause / crash site")
    exploitability: Severity
    root_cause: str


def analyze(client: AugClient, sanitizer_output: str) -> CrashAnalysis:
    # TODO: prompt the model over the ASan/traceback to classify the bug, derive
    # a stable dedup_key from the crashing frame, rate exploitability, and explain
    # the root cause. return client.reason(prompt, CrashAnalysis)
    raise NotImplementedError("Build the crash-triage prompt.")


if __name__ == "__main__":
    print("Feed a folder of sanitizer outputs; dedup by .dedup_key. See reference.")

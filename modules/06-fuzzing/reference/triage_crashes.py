"""REFERENCE — crash triage / dedup / root-cause (worked answer)."""

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


_PROMPT = """Triage this crash from its sanitizer/traceback output. Classify the
bug, derive a STABLE dedup_key from the crashing function + offending operation
(so byte-different inputs hitting the same bug share a key), rate exploitability
(write-what-where is critical; null-deref is usually low), and explain the root
cause pointing at the offending frame.

Crash output:
{crash}"""


def analyze(client: AugClient, sanitizer_output: str) -> CrashAnalysis:
    return client.reason(_PROMPT.format(crash=sanitizer_output[:6000]), CrashAnalysis)


def main() -> None:
    crash_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    client = AugClient()
    seen: dict[str, CrashAnalysis] = {}
    for f in sorted(crash_dir.glob("*.txt")):
        a = analyze(client, f.read_text(errors="replace"))
        if a.dedup_key not in seen:
            seen[a.dedup_key] = a
    print(f"{len(seen)} distinct bug(s):")
    for k, a in seen.items():
        print(f"  [{a.exploitability.value}] {a.bug_class} ({k}) — {a.root_cause}")


if __name__ == "__main__":
    main()

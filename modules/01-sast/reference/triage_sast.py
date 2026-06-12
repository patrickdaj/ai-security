"""REFERENCE — completed SAST triage with enclosing-function enrichment.

The project stub leaves enrichment as a line-window; this version pulls the
*enclosing function*, which sharpens the model's reachability reasoning. Compare
after you've built your own.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

_SEV = {"INFO": Severity.info, "WARNING": Severity.medium, "ERROR": Severity.high}


def enclosing_function(path: str, line: int) -> str:
    """Walk upward to the nearest def/class header, return that block to the hit."""
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return ""
    start = 0
    for i in range(min(line, len(lines)) - 1, -1, -1):
        s = lines[i].lstrip()
        if s.startswith(("def ", "class ", "async def ")):
            start = i
            break
    end = min(len(lines), line + 5)
    return "\n".join(f"{i + 1:>5} {lines[i]}" for i in range(start, end))


def from_semgrep(r: dict) -> Finding:
    path, line = r.get("path", "?"), r.get("start", {}).get("line", 0)
    extra = r.get("extra", {})
    return Finding(
        tool="semgrep",
        rule_id=r.get("check_id", "?"),
        title=(extra.get("message", "") or r.get("check_id", ""))[:120],
        severity=_SEV.get(extra.get("severity", "WARNING"), Severity.medium),
        location=f"{path}:{line}",
        description=extra.get("message", ""),
        context=enclosing_function(path, line),
        raw=r,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("findings_json")
    ap.add_argument("--min-confidence", type=float, default=0.7)
    args = ap.parse_args()
    data = json.loads(Path(args.findings_json).read_text())
    client = AugClient()
    for r in data.get("results", []):
        f = from_semgrep(r)
        t = triage_finding(client, f)
        if t.confidence < args.min_confidence:
            continue
        print(f"[{t.verdict.value}] {f.rule_id} @ {f.location} "
              f"({f.severity.value}->{t.adjusted_severity.value}, {t.confidence:.2f})")
        print(f"  {t.rationale}")
        if t.suggested_fix:
            print(f"  fix: {t.suggested_fix}")


if __name__ == "__main__":
    main()

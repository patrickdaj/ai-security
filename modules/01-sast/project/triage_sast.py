"""Auto-triage Semgrep/Bandit findings with Claude.

Usage:
    python triage_sast.py scratch/semgrep.json [--min-confidence 0.7] [--fast]

This is a starter. The TODOs are the actual learning — especially enrichment,
which is what makes the triage good. See the module README.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make the repo-root `aug` package importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

_SEMGREP_SEV = {
    "INFO": Severity.info,
    "WARNING": Severity.medium,
    "ERROR": Severity.high,
}


def read_context(path: str, line: int, window: int = 15) -> str:
    """Pull a window of source around the hit. TODO: upgrade to the *enclosing
    function* via tree-sitter for much better reachability reasoning."""
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return ""
    lo = max(0, line - window)
    hi = min(len(lines), line + window)
    return "\n".join(f"{i + 1:>5} {lines[i]}" for i in range(lo, hi))


def from_semgrep(result: dict) -> Finding:
    path = result.get("path", "?")
    line = result.get("start", {}).get("line", 0)
    extra = result.get("extra", {})
    sev = _SEMGREP_SEV.get(extra.get("severity", "WARNING"), Severity.medium)
    return Finding(
        tool="semgrep",
        rule_id=result.get("check_id", "?"),
        title=extra.get("message", "")[:120] or result.get("check_id", "?"),
        severity=sev,
        location=f"{path}:{line}",
        description=extra.get("message", ""),
        context=read_context(path, line),
        raw=result,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("findings_json", help="Semgrep --json output")
    ap.add_argument("--min-confidence", type=float, default=0.0)
    ap.add_argument("--fast", action="store_true", help="Use the cheap model")
    args = ap.parse_args()

    data = json.loads(Path(args.findings_json).read_text())
    findings = [from_semgrep(r) for r in data.get("results", [])]
    print(f"Loaded {len(findings)} findings. Triaging...\n")

    client = AugClient()
    kept = 0
    for f in findings:
        t = triage_finding(client, f, fast=args.fast)
        if t.confidence < args.min_confidence:
            continue
        kept += 1
        print(f"[{t.verdict.value}] {f.rule_id} @ {f.location}")
        print(f"  severity: {f.severity.value} -> {t.adjusted_severity.value}  "
              f"(conf {t.confidence:.2f})")
        print(f"  {t.rationale}")
        if t.suggested_fix:
            print(f"  fix: {t.suggested_fix}")
        print()

    print(f"Kept {kept}/{len(findings)} at confidence >= {args.min_confidence}")


if __name__ == "__main__":
    main()

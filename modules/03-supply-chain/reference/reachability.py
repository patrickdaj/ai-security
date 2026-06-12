"""REFERENCE — SBOM reachability triage (worked answer)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

_SEV = {"Low": Severity.low, "Medium": Severity.medium, "High": Severity.high,
        "Critical": Severity.critical, "Negligible": Severity.info, "Unknown": Severity.info}


def import_sites(package: str, code_root: str = ".") -> str:
    """Cheap reachability evidence: where is the affected package imported?"""
    hits = []
    for p in Path(code_root).rglob("*.py"):
        try:
            for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
                if f"import {package}" in line or f"from {package}" in line:
                    hits.append(f"{p}:{n}: {line.strip()}")
        except OSError:
            continue
    return "\n".join(hits[:20]) or "(no direct imports of this package found)"


def from_grype(match: dict, code_root: str = ".") -> Finding:
    v = match.get("vulnerability", {})
    artifact = match.get("artifact", {})
    pkg = artifact.get("name", "?")
    return Finding(
        tool="grype",
        rule_id=v.get("id", "?"),
        title=v.get("description", v.get("id", ""))[:120],
        severity=_SEV.get(v.get("severity", "Unknown"), Severity.info),
        location=f"{pkg}@{artifact.get('version', '?')}",
        description=v.get("description", ""),
        context=f"ADVISORY: {v.get('description', '')[:800]}\n\nIMPORT SITES:\n"
                + import_sites(pkg, code_root),
        raw={"id": v.get("id"), "pkg": pkg},
    )


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    client = AugClient()
    for m in data.get("matches", []):
        f = from_grype(m)
        t = triage_finding(client, f)
        if t.verdict.value == "false_positive":
            continue
        print(f"[{t.adjusted_severity.value}] {f.rule_id} {f.location} "
              f"({t.verdict.value}, {t.confidence:.2f}) — {t.rationale}")


if __name__ == "__main__":
    main()

"""Render pipeline results to Markdown + JSON.

A result is a (Finding, Triage | None) pair — the triage is None when the
pipeline ran with --no-triage (aggregation only).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from aug import Finding, Severity, Triage

Result = tuple[Finding, "Triage | None"]

_ORDER = [Severity.critical, Severity.high, Severity.medium, Severity.low, Severity.info]


def _sev(result: Result) -> Severity:
    finding, triage = result
    return triage.adjusted_severity if triage else finding.severity


def sort_results(results: list[Result]) -> list[Result]:
    return sorted(results, key=lambda r: _ORDER.index(_sev(r)))


def to_json(results: list[Result]) -> str:
    payload = [
        {
            "finding": f.model_dump(mode="json", exclude={"raw"}),
            "triage": t.model_dump(mode="json") if t else None,
        }
        for f, t in results
    ]
    return json.dumps(payload, indent=2)


def to_markdown(results: list[Result], target: str) -> str:
    results = sort_results(results)
    triaged = any(t for _, t in results)
    lines = [
        f"# Security Pipeline Report — `{target}`",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')} · "
        f"{len(results)} findings"
        + (" · triaged with `aug`" if triaged else " · aggregation only (no triage)"),
        "",
    ]
    counts: dict[Severity, int] = {}
    for r in results:
        counts[_sev(r)] = counts.get(_sev(r), 0) + 1
    lines.append("| Severity | Count |")
    lines.append("|----------|------:|")
    for s in _ORDER:
        if counts.get(s):
            lines.append(f"| {s.value} | {counts[s]} |")
    lines.append("")

    for f, t in results:
        sev = _sev((f, t))
        lines.append(f"## [{sev.value}] {f.tool}: {f.rule_id}")
        lines.append(f"- **Location:** `{f.location}`")
        if t:
            lines.append(
                f"- **Verdict:** {t.verdict.value} "
                f"(severity {f.severity.value} → {t.adjusted_severity.value}, "
                f"conf {t.confidence:.2f})"
            )
            lines.append(f"- **Why:** {t.rationale}")
            if t.suggested_fix:
                lines.append(f"- **Fix:** {t.suggested_fix}")
        else:
            lines.append(f"- {f.title}")
        lines.append("")
    return "\n".join(lines)

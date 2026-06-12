"""Scanner adapters: run a deterministic tool, normalize to `aug.Finding`.

Each adapter shells out to a security tool and maps its native output into the
shared schema. Adapters are resilient: a missing tool or a parse error yields an
empty list and a logged skip, never a crash — so the pipeline runs with whatever
is installed.

Add a scanner by writing one function `(target: str) -> list[Finding]` and
registering it in REGISTRY.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

from aug import Finding, Severity

log = logging.getLogger("automation.scanners")

_SEMGREP_SEV = {"INFO": Severity.info, "WARNING": Severity.medium, "ERROR": Severity.high}
_TRIVY_SEV = {
    "UNKNOWN": Severity.info,
    "LOW": Severity.low,
    "MEDIUM": Severity.medium,
    "HIGH": Severity.high,
    "CRITICAL": Severity.critical,
}


def _have(tool: str) -> bool:
    if shutil.which(tool):
        return True
    log.warning("skipping %s: not installed (PATH)", tool)
    return False


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    # Many scanners exit non-zero precisely when they find something; we parse
    # stdout regardless of return code.
    return subprocess.run(cmd, capture_output=True, text=True)


def _context(path: str, line: int, window: int = 12) -> str:
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return ""
    lo, hi = max(0, line - window), min(len(lines), line + window)
    return "\n".join(f"{i + 1:>5} {lines[i]}" for i in range(lo, hi))


def semgrep(target: str) -> list[Finding]:
    if not _have("semgrep"):
        return []
    proc = _run(["semgrep", "--config", "auto", "--json", "--quiet", target])
    try:
        results = json.loads(proc.stdout).get("results", [])
    except json.JSONDecodeError:
        log.warning("semgrep produced no parseable JSON")
        return []
    out = []
    for r in results:
        path, line = r.get("path", "?"), r.get("start", {}).get("line", 0)
        extra = r.get("extra", {})
        out.append(
            Finding(
                tool="semgrep",
                rule_id=r.get("check_id", "?"),
                title=(extra.get("message", "") or r.get("check_id", ""))[:120],
                severity=_SEMGREP_SEV.get(extra.get("severity", "WARNING"), Severity.medium),
                location=f"{path}:{line}",
                description=extra.get("message", ""),
                context=_context(path, line),
                raw=r,
            )
        )
    return out


def gitleaks(target: str) -> list[Finding]:
    if not _have("gitleaks"):
        return []
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        report = tf.name
    _run(["gitleaks", "detect", "--source", target, "--no-banner",
          "--report-format", "json", "--report-path", report])
    try:
        leaks = json.loads(Path(report).read_text() or "[]")
    except (OSError, json.JSONDecodeError):
        return []
    out = []
    for lk in leaks:
        # Deliberately do NOT put the raw secret in context — reports may be
        # committed/uploaded. Keep rule + location only.
        out.append(
            Finding(
                tool="gitleaks",
                rule_id=lk.get("RuleID", "secret"),
                title=lk.get("Description", "Potential secret")[:120],
                severity=Severity.high,
                location=f"{lk.get('File', '?')}:{lk.get('StartLine', 0)}",
                description="A high-entropy/known-pattern secret was matched (value redacted).",
                context=f"rule={lk.get('RuleID')} file={lk.get('File')} commit={lk.get('Commit', '')}",
                raw={k: v for k, v in lk.items() if k not in ("Secret", "Match")},
            )
        )
    return out


def trivy(target: str) -> list[Finding]:
    if not _have("trivy"):
        return []
    proc = _run(["trivy", "fs", "--quiet", "--format", "json", target])
    try:
        results = json.loads(proc.stdout).get("Results", []) or []
    except json.JSONDecodeError:
        return []
    out = []
    for res in results:
        for v in res.get("Vulnerabilities", []) or []:
            out.append(
                Finding(
                    tool="trivy",
                    rule_id=v.get("VulnerabilityID", "?"),
                    title=(v.get("Title") or v.get("VulnerabilityID", ""))[:120],
                    severity=_TRIVY_SEV.get(v.get("Severity", "UNKNOWN"), Severity.info),
                    location=f"{v.get('PkgName', '?')}@{v.get('InstalledVersion', '?')}",
                    description=v.get("Description", "")[:1500],
                    context=f"fixed_in={v.get('FixedVersion', 'n/a')} ref={v.get('PrimaryURL', '')}",
                    raw={k: v.get(k) for k in ("VulnerabilityID", "PkgName", "Severity")},
                )
            )
    return out


REGISTRY: dict[str, Callable[[str], list[Finding]]] = {
    "semgrep": semgrep,
    "gitleaks": gitleaks,
    "trivy": trivy,
}

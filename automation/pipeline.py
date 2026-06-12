"""The headless pipeline: scan -> normalize -> triage -> report -> exit code.

Designed to run unattended (CI, cron, a CodeBuild job). Configurable via a YAML
file or pure CLI flags; runs with zero config using sensible defaults.

    python -m automation --target . --out scratch/pipeline
    aug-pipeline --config automation.yaml --fail-on high

Exit code: 0 unless a kept finding meets/exceeds `--fail-on` severity — so it
gates a build. Use --no-triage to aggregate without a model (CI without a key).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

from automation import report
from automation.report import Result
from automation.scanners import REGISTRY
from aug import Finding, Severity

log = logging.getLogger("automation.pipeline")

_ORDER = [Severity.info, Severity.low, Severity.medium, Severity.high, Severity.critical]

DEFAULTS = {
    "target": ".",
    "scanners": list(REGISTRY),
    "out": "scratch/pipeline",
    "fail_on": "high",
    "min_confidence": 0.0,
    "fast": False,
    "triage": True,
}


def load_config(path: str | None) -> dict:
    cfg = dict(DEFAULTS)
    if path and Path(path).exists():
        cfg.update(yaml.safe_load(Path(path).read_text()) or {})
    return cfg


def collect(scanners: list[str], target: str) -> list[Finding]:
    findings: list[Finding] = []
    for name in scanners:
        fn = REGISTRY.get(name)
        if not fn:
            log.warning("unknown scanner '%s' (have: %s)", name, ", ".join(REGISTRY))
            continue
        found = fn(target)
        log.info("%s: %d findings", name, len(found))
        findings.extend(found)
    return findings


def triage(findings: list[Finding], *, fast: bool, min_confidence: float) -> list[Result]:
    """Triage with the model. Falls back to aggregation-only if no backend."""
    try:
        from aug import AugClient
        from aug.triage import triage_finding

        client = AugClient()
    except Exception as e:  # noqa: BLE001 - no key/SDK/daemon -> degrade, don't crash
        log.warning("triage unavailable (%s); producing aggregation-only report", e)
        return [(f, None) for f in findings]

    results: list[Result] = []
    for f in findings:
        try:
            t = triage_finding(client, f, fast=fast)
        except Exception as e:  # noqa: BLE001 - one bad finding shouldn't sink the run
            log.warning("triage failed for %s: %s", f.rule_id, e)
            results.append((f, None))
            continue
        if t.confidence >= min_confidence:
            results.append((f, t))
    return results


def gate_exit_code(results: list[Result], fail_on: str) -> int:
    threshold = _ORDER.index(Severity(fail_on))
    for f, t in results:
        sev = t.adjusted_severity if t else f.severity
        # An aggregation-only finding only gates if it's a confirmed-or-better
        # severity; with triage, false positives have already been dropped here
        # only when they cleared min_confidence — verdict still matters.
        if t and t.verdict.value == "false_positive":
            continue
        if _ORDER.index(sev) >= threshold:
            return 1
    return 0


def run_pipeline(cfg: dict) -> int:
    findings = collect(cfg["scanners"], cfg["target"])
    log.info("collected %d findings total", len(findings))

    if cfg["triage"]:
        results = triage(findings, fast=cfg["fast"], min_confidence=cfg["min_confidence"])
    else:
        results = [(f, None) for f in findings]

    out = Path(cfg["out"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(report.to_markdown(results, cfg["target"]))
    (out / "report.json").write_text(report.to_json(results))
    log.info("wrote %s/report.md and report.json", out)

    code = gate_exit_code(results, cfg["fail_on"])
    log.info("gate: fail_on=%s -> exit %d", cfg["fail_on"], code)
    return code


def main() -> None:
    ap = argparse.ArgumentParser(description="Headless security scan + AI triage pipeline.")
    ap.add_argument("--config", help="YAML config (optional; CLI flags override)")
    ap.add_argument("--target", help="Path/repo to scan")
    ap.add_argument("--scanners", help="Comma-separated subset, e.g. 'semgrep,trivy'")
    ap.add_argument("--out", help="Output directory")
    ap.add_argument("--fail-on", choices=[s.value for s in Severity], help="Exit 1 at/above this")
    ap.add_argument("--min-confidence", type=float, help="Drop triaged findings below this")
    ap.add_argument("--fast", action="store_true", help="Use the cheap/fast model")
    ap.add_argument("--no-triage", action="store_true", help="Aggregate only; skip the model")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    cfg = load_config(args.config)
    if args.target:
        cfg["target"] = args.target
    if args.scanners:
        cfg["scanners"] = [s.strip() for s in args.scanners.split(",") if s.strip()]
    if args.out:
        cfg["out"] = args.out
    if args.fail_on:
        cfg["fail_on"] = args.fail_on
    if args.min_confidence is not None:
        cfg["min_confidence"] = args.min_confidence
    if args.fast:
        cfg["fast"] = True
    if args.no_triage:
        cfg["triage"] = False

    sys.exit(run_pipeline(cfg))


if __name__ == "__main__":
    main()

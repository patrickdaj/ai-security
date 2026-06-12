"""automation — headless orchestration for the security toolchain.

This is the capstone workflow as real, runnable automation: run a set of
scanners against a target, normalize everything into `aug.Finding`, triage with
Claude (or a local model), and emit JSON + Markdown reports — with a
severity-based exit code so it gates CI.

It degrades gracefully: a scanner that isn't installed is skipped, and if no
model backend is reachable (e.g. CI without an API key) it still produces an
aggregated report with `--no-triage`.

Entry points:
    python -m automation [--config automation.yaml] [--target .] [--no-triage]
    aug-pipeline ...            # console script (see pyproject)
"""

from automation.pipeline import run_pipeline

__all__ = ["run_pipeline"]

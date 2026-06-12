"""STUB — SBOM reachability triage. Reference: ../reference/.

Build the Grype/OSV -> Finding adapter (advisory text + your import sites into
.context), then triage — the shared engine already reasons about reachability.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402
from aug.triage import triage_finding  # noqa: E402

_SEV = {"Low": Severity.low, "Medium": Severity.medium, "High": Severity.high,
        "Critical": Severity.critical}


def from_grype(match: dict) -> Finding:
    # TODO: map a Grype match -> Finding. Pull the CVE id, severity, the
    # package@version into `location`, and the advisory description + any import
    # sites of the affected package into `context` (that's what enables the
    # reachability call).
    raise NotImplementedError("Build the Grype -> Finding adapter.")


def main() -> None:
    # TODO: load grype JSON, map each match, triage_finding(), print reachable ones.
    print("See the reference for the full flow.")


if __name__ == "__main__":
    main()

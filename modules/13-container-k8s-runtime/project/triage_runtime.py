"""STUB — Falco/Tetragon runtime-alert triage. Reference: ../reference/.

Collapse the firehose into incidents. The `dedup_key` (from root cause, not
input) is what makes 1,000 benign alerts become two named clusters.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, RuntimeIncident  # noqa: E402


def triage(client: AugClient, alert: dict) -> RuntimeIncident:
    # TODO: prompt the model over the Falco alert (rule, process tree, syscall
    # context) for a verdict, a stable dedup_key, the ATT&CK technique, and the
    # next step. return client.reason(prompt, RuntimeIncident)
    raise NotImplementedError("Build the runtime-triage prompt.")


if __name__ == "__main__":
    print("Stream Falco JSON, triage, dedup by .dedup_key. See the reference.")

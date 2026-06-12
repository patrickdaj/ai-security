"""REFERENCE — Falco runtime-alert triage (worked answer)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, RuntimeIncident  # noqa: E402

_PROMPT = """Triage this Falco runtime alert. Decide if it's a real incident or
benign, derive a STABLE dedup_key from the root cause (rule + the process/path
pattern, NOT the timestamp/pid, so repeats collapse), map to a MITRE ATT&CK
technique if you can, and give the next investigative step.

Alert:
```json
{alert}
```"""


def triage(client: AugClient, alert: dict) -> RuntimeIncident:
    return client.reason(_PROMPT.format(alert=json.dumps(alert, indent=2)[:3000]),
                         RuntimeIncident)


def main() -> None:
    # Falco emits one JSON object per line.
    lines = Path(sys.argv[1]).read_text().splitlines()
    client = AugClient()
    incidents: dict[str, RuntimeIncident] = {}
    for line in lines:
        if not line.strip():
            continue
        inc = triage(client, json.loads(line))
        incidents.setdefault(inc.dedup_key, inc)
    real = [i for i in incidents.values() if i.verdict.value == "true_positive"]
    print(f"{len(lines)} alerts -> {len(incidents)} clusters, {len(real)} incident(s):")
    for i in real:
        print(f"  [{i.severity.value}] {i.dedup_key} ({i.attack_technique}) — {i.summary}")
        print(f"     next: {i.next_step}")


if __name__ == "__main__":
    main()

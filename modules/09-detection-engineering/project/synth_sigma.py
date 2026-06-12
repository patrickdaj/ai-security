"""STUB — threat intel -> Sigma rule. Reference: ../reference/.

Validate with `sigma check` and convert with `sigma convert -t <backend>`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402


def synthesize(client: AugClient, threat_intel: str) -> PolicyDraft:
    # TODO: prompt for a valid Sigma rule (language='sigma') from the intel —
    # correct logsource, a TIGHT detection block, ATT&CK tags. Avoid overbroad
    # selections. return client.reason(prompt, PolicyDraft)
    raise NotImplementedError("Build the Sigma synthesis prompt.")


if __name__ == "__main__":
    print(synthesize(AugClient(), Path(sys.argv[1]).read_text()).policy)

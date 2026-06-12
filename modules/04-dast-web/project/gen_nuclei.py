"""STUB — advisory -> Nuclei template. Reference: ../reference/.

Generate typed fields, render YAML, then validate with `nuclei -validate`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402


def generate(client: AugClient, advisory: str) -> PolicyDraft:
    # TODO: prompt the model to produce a Nuclei template (language='nuclei')
    # from the advisory — the request path, matchers, and severity. Put the YAML
    # in PolicyDraft.policy. Then: return client.reason(prompt, PolicyDraft)
    raise NotImplementedError("Build the advisory -> Nuclei template prompt.")


if __name__ == "__main__":
    advisory = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
    print(generate(AugClient(), advisory).policy)

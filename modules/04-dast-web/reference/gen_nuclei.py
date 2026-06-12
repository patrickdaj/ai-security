"""REFERENCE — advisory -> Nuclei template (worked answer).

Validate the output: `nuclei -validate -t generated.yaml`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402

_PROMPT = """Generate a valid Nuclei template (current YAML syntax) that detects
the issue in this advisory. Include: an `id`, an `info` block (name, author,
severity, description, tags), and an `http` request with precise `matchers`
(status + body/header words) using `matchers-condition: and` to avoid false
positives. Put the rendered YAML in PolicyDraft.policy, language='nuclei', and
give allow/deny test_cases (a vulnerable vs patched response).

Advisory:
{advisory}"""


def generate(client: AugClient, advisory: str) -> PolicyDraft:
    return client.reason(_PROMPT.format(advisory=advisory), PolicyDraft)


def main() -> None:
    advisory = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    draft = generate(AugClient(), advisory)
    out = Path("scratch/generated.nuclei.yaml")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(draft.policy + "\n")
    print(f"wrote {out}\nintent: {draft.intent}\nvalidate: nuclei -validate -t {out}")


if __name__ == "__main__":
    main()

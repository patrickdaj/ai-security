"""REFERENCE — threat intel -> Sigma rule (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402

_PROMPT = """Generate a valid Sigma rule from this threat intel. Pick the correct
`logsource`, write a TIGHT `detection` block (avoid broad selections that bury
the SOC in false positives), include a precise `condition`, ATT&CK `tags`, a
`level`, and `falsepositives`. Put the rendered YAML in PolicyDraft.policy,
language='sigma', and give a should-match and should-not-match test case.

Threat intel:
{intel}"""


def synthesize(client: AugClient, threat_intel: str) -> PolicyDraft:
    return client.reason(_PROMPT.format(intel=threat_intel[:6000]), PolicyDraft)


def main() -> None:
    intel = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    draft = synthesize(AugClient(), intel)
    out = Path("scratch/generated.sigma.yml")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(draft.policy + "\n")
    print(f"wrote {out}\nvalidate: sigma check {out}")


if __name__ == "__main__":
    main()

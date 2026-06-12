"""REFERENCE — secret classification (worked answer).

Classifies on path + context only; the raw secret never leaves the host.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Severity  # noqa: E402


class SecretVerdict(BaseModel):
    kind: str = Field(description="live | test_or_example | already_rotated | false_positive")
    is_live_guess: bool
    blast_radius: Severity
    rotate_now: bool
    rationale: str


_PROMPT = """Classify this secret-scanner hit WITHOUT seeing the secret value.

Rule: {rule}
File: {file}:{line}
Surrounding context (value redacted): {context}

Use the path as a strong prior: hits under tests/, examples/, fixtures/, docs/,
or *.md are usually test/example values; hits in config/, prod, or deploy paths
are more likely live. Decide kind, whether it's likely live, the blast radius if
it is, and whether to rotate now."""


def classify(client: AugClient, hit: dict) -> SecretVerdict:
    prompt = _PROMPT.format(
        rule=hit.get("RuleID", "?"),
        file=hit.get("File", "?"),
        line=hit.get("StartLine", 0),
        context=f"path={hit.get('File')} commit={hit.get('Commit', '')}",
    )
    return client.reason(prompt, SecretVerdict)


def main() -> None:
    hits = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else []
    client = AugClient()
    for h in hits:
        v = classify(client, h)
        flag = "ROTATE NOW" if v.rotate_now else "ok"
        print(f"[{v.kind}] {h.get('File')}:{h.get('StartLine')} "
              f"blast={v.blast_radius.value} {flag} — {v.rationale}")


if __name__ == "__main__":
    main()

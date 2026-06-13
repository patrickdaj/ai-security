"""REFERENCE — intent -> SIEM detection query (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft  # noqa: E402

_PROMPT = """Write a precise {backend} detection query for this intent, tight
enough to avoid burying the SOC in false positives. Use the right data
source/index and fields for {backend} (SPL=index/sourcetype, EQL=event
categories, KQL=table names). Put the rendered query in PolicyDraft.policy,
language='{backend}', and give a should-match and should-not-match example.

Intent: {intent}"""


def generate(client: AugClient, intent: str, backend: str = "spl") -> PolicyDraft:
    return client.reason(_PROMPT.format(backend=backend, intent=intent), PolicyDraft)


def main() -> None:
    backend = sys.argv[1] if len(sys.argv) > 1 else "spl"
    intent = sys.argv[2] if len(sys.argv) > 2 else "An IAM user was granted AdministratorAccess"
    draft = generate(AugClient(), intent, backend)
    print(f"# {draft.intent}\n{draft.policy}")
    for tc in draft.test_cases:
        print(f"# test: {tc}")


if __name__ == "__main__":
    main()

"""REFERENCE — decompiled-function analysis (worked answer).

Wire `renames` back into Ghidra via a headless post-script; gate global renames.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient  # noqa: E402


class FunctionAnalysis(BaseModel):
    summary: str
    suggested_name: str
    role: str = Field(description="parser | crypto | network | auth | alloc | ...")
    renames: dict[str, str] = Field(description="old_var -> meaningful_name")
    security_notes: list[str]


_PROMPT = """You are reverse-engineering a binary. Here is one function's
decompiled pseudo-C (accurate but unlabeled). Describe what it does in one or two
sentences, propose a meaningful function name and variable renames, classify its
role, and flag any security-relevant patterns (unbounded copy, hardcoded
key/secret, weak comparison, integer overflow). You are DESCRIBING the code, not
executing it.

```c
{code}
```"""


def analyze(client: AugClient, pseudo_c: str) -> FunctionAnalysis:
    return client.reason(_PROMPT.format(code=pseudo_c[:6000]), FunctionAnalysis)


def main() -> None:
    a = analyze(AugClient(), Path(sys.argv[1]).read_text())
    print(f"{a.suggested_name}  [{a.role}]\n{a.summary}")
    for old, new in a.renames.items():
        print(f"  rename {old} -> {new}")
    for n in a.security_notes:
        print(f"  ! {n}")


if __name__ == "__main__":
    main()

"""STUB — summarize a decompiled function + suggest names. Reference: ../reference/.

Input is decompiled pseudo-C (from Ghidra/r2). You're describing untrusted code,
not running it.
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


def analyze(client: AugClient, pseudo_c: str) -> FunctionAnalysis:
    # TODO: prompt the model to summarize the function, propose a name + variable
    # renames, guess its role, and flag security-relevant patterns (unbounded
    # copy, hardcoded key, weak check). return client.reason(prompt, FunctionAnalysis)
    raise NotImplementedError("Build the decompiled-function analysis prompt.")


if __name__ == "__main__":
    print(analyze(AugClient(), Path(sys.argv[1]).read_text()))

"""REFERENCE — crypto-misuse scanner (worked answer)."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Remediation, Severity  # noqa: E402


class CryptoFinding(BaseModel):
    issue: str
    location: str
    severity: Severity
    remediation: Remediation


class CryptoReport(BaseModel):
    findings: list[CryptoFinding]


_PROMPT = """Review this code for CRYPTOGRAPHIC MISUSE — the failures are in how
crypto is used, not the algorithms. Look for: ECB mode, static/reused IVs,
hardcoded keys, MD5/SHA-1 (or unsalted/fast hashes) for passwords, weak RNG for
secrets, missing authenticated encryption, disabled cert verification, and
home-grown crypto. For each, give the issue, location, severity, and a
Remediation with the correct construction as a diff (e.g. AES-GCM with a random
nonce; argon2/bcrypt for passwords). Don't flag correct usage.

Code:
```
{code}
```"""


def scan(client: AugClient, code: str) -> CryptoReport:
    return client.reason(_PROMPT.format(code=code[:10000]), CryptoReport, max_tokens=12000)


def main() -> None:
    code = Path(sys.argv[1]).read_text(errors="replace") if len(sys.argv) > 1 else ""
    rep = scan(AugClient(), code)
    for f in rep.findings:
        print(f"[{f.severity.value}] {f.issue} @ {f.location}")
        print(f.remediation.patch)


if __name__ == "__main__":
    main()

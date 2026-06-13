"""STUB — crypto-misuse scanner. Reference: ../reference/.

Find the crypto that fails in the *using*, and produce the correct fix.
"""

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


def scan(client: AugClient, code: str) -> CryptoReport:
    # TODO: prompt the model to find crypto misuse (ECB, static IV/key, MD5/SHA1
    # for passwords, weak RNG, missing auth-encryption) and produce a Remediation
    # (correct construction + diff) for each. return client.reason(prompt, CryptoReport)
    raise NotImplementedError("Build the crypto-misuse prompt.")


if __name__ == "__main__":
    print("Feed source files. See the reference.")

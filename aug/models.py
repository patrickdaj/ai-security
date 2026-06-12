"""Common schemas shared across modules.

Every tool we tour (Semgrep, Grype, Nuclei, Zeek, ...) emits findings in its
own format. The first job of any augmentation is to *normalize* into these
types so the reasoning layer sees one shape. The model's structured output is
also validated against these, so what comes back is typed, not prose.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Finding(BaseModel):
    """A single normalized finding from any tool.

    Modules write small adapters (`from_semgrep`, `from_grype`, ...) that map a
    tool's native output into this. Keep `raw` around so nothing is lost.
    """

    tool: str = Field(description="Tool that produced the finding, e.g. 'semgrep'.")
    rule_id: str = Field(description="Tool-native rule/check identifier.")
    title: str
    severity: Severity
    location: str = Field(
        description="Where it was found: 'path:line', a URL, a package@version, etc."
    )
    description: str = ""
    # Surrounding context the model needs to judge the finding. For SAST this is
    # the code snippet; for a scanner, the request/response; for a CVE, the
    # advisory text. Enrichment fills this in before reasoning.
    context: str = ""
    raw: dict = Field(default_factory=dict, description="Untouched tool output.")


class TriageVerdict(str, Enum):
    true_positive = "true_positive"
    false_positive = "false_positive"
    needs_review = "needs_review"


class Triage(BaseModel):
    """The model's structured judgment about a finding.

    This is what an augmentation returns instead of free text — so it can be
    sorted, filtered, gated on confidence, and fed into a ticketing system.
    """

    verdict: TriageVerdict
    # Re-rated severity in context (the tool's static severity is often wrong
    # once you account for reachability/exposure).
    adjusted_severity: Severity
    confidence: float = Field(ge=0.0, le=1.0, description="0..1 model confidence.")
    rationale: str = Field(description="Why — grounded in the provided context.")
    exploitability: str = Field(
        default="", description="Short note on how/whether this is reachable."
    )
    suggested_fix: str = Field(
        default="", description="Concrete remediation, ideally as a diff or code."
    )

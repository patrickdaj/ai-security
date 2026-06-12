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


# --------------------------------------------------------------------------
# Infrastructure & Runtime phase (modules 11-15) schemas.
# These extend the same idea: the model reasons over normalized evidence and
# returns a typed result a pipeline can gate on.
# --------------------------------------------------------------------------


class Remediation(BaseModel):
    """A generated, review-ready fix. Used by IaC (08), CI/CD (12), and host
    hardening (14). The breaking-change risk is the gate: auto-apply low risk,
    hold high risk for a human."""

    patch: str = Field(description="The fix, ideally a unified diff or exact config.")
    breaking_change_risk: Severity = Field(
        description="How likely this change breaks something in production."
    )
    explanation: str
    compliance_controls: list[str] = Field(
        default_factory=list,
        description="Controls this satisfies, e.g. ['CIS-1.2', 'SOC2-CC6.1'].",
    )


class AttackPathStep(BaseModel):
    principal: str = Field(description="Identity/resource at this hop.")
    action: str = Field(description="The permission/edge that enables the next hop.")


class AttackPath(BaseModel):
    """A privilege-escalation or lateral-movement path through cloud IAM / a
    graph of assets. Produced by the CIEM module (11) and emulation work."""

    entrypoint: str = Field(description="Where an attacker starts (e.g. a leaked role).")
    target: str = Field(description="What they reach (e.g. admin / sensitive bucket).")
    steps: list[AttackPathStep]
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    narrative: str = Field(description="Plain-language walkthrough an analyst can act on.")
    least_privilege_fix: str = Field(
        default="", description="The minimal policy change that breaks the path."
    )


class PolicyDraft(BaseModel):
    """A generated authorization / admission / microsegmentation policy.
    Used by CIEM (11), K8s runtime (13: Kyverno/Rego), and ZTNA (15:
    Oathkeeper/Pomerium/OPA). Generate typed fields, then render + validate the
    policy — never trust un-validated policy text."""

    language: str = Field(description="rego | kyverno | pomerium | oathkeeper | ...")
    intent: str = Field(description="The natural-language goal this enforces.")
    policy: str = Field(description="The rendered policy source.")
    test_cases: list[str] = Field(
        default_factory=list,
        description="Allow/deny cases the author should verify the policy against.",
    )
    notes: str = ""


class RuntimeIncident(BaseModel):
    """Triage of a runtime alert (Falco/Tetragon/osquery). Collapses noisy,
    repetitive alerts into an incident with a verdict and next step. Used by
    the K8s runtime (13) and detection (09) modules."""

    verdict: TriageVerdict
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = Field(description="What happened, grounded in the alert evidence.")
    dedup_key: str = Field(
        description="Stable key derived from root cause so duplicates collapse."
    )
    next_step: str = Field(default="", description="The recommended investigative action.")
    attack_technique: str = Field(
        default="", description="MITRE ATT&CK technique id if identifiable."
    )

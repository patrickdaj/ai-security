"""STARTER STUB — cross-tool correlation.

The single most valuable thing the pipeline can't yet do: notice when findings
from *different* tools describe the same underlying risk, and reason about the
combined exposure. A SAST injection bug + a reachable CVE in the same service +
an over-permissioned role for that service is one critical, not three mediums.

Your task: group findings by a shared key (file path, package, service, or
endpoint), then ask the model to assess each cluster's combined risk. The
pipeline (automation/pipeline.py) is where you'd call this after triage.

See the capstone's example-output/security-report.md for the target shape.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, Finding, Severity  # noqa: E402


class CorrelatedRisk(BaseModel):
    """The model's verdict on a cluster of related findings."""

    title: str
    combined_severity: Severity = Field(
        description="Severity of the findings *together*, which may exceed any one alone."
    )
    member_rule_ids: list[str]
    narrative: str = Field(description="Why these are one risk, grounded in the evidence.")
    fix_order: list[str] = Field(description="The order to remediate, most urgent first.")


def correlation_key(finding: Finding) -> str:
    """TODO: derive the join key. Reasonable starting points:
      - the file path (strip the :line) for code findings
      - the package@version for dependency findings
      - the service/endpoint for runtime/web findings
    Tune this — the quality of correlation is mostly the quality of this key."""
    return finding.location.split(":")[0]


def correlate(client: AugClient, findings: list[Finding]) -> list[CorrelatedRisk]:
    clusters: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        clusters[correlation_key(f)].append(f)

    risks: list[CorrelatedRisk] = []
    for key, group in clusters.items():
        if len(group) < 2:
            continue  # a cluster of one isn't a correlation
        # TODO: build a prompt that hands the model the grouped findings (tool,
        # rule, severity, context) and asks for a CorrelatedRisk — whether they
        # compound, the combined severity, and the fix order. Then:
        #   risks.append(client.reason(prompt, CorrelatedRisk))
        raise NotImplementedError(f"Assess combined risk for cluster '{key}'.")
    return risks

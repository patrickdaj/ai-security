"""Generic, tool-agnostic finding triage.

This is the workhorse used by the SAST, secrets, supply-chain, and DAST
modules. Given a normalized `Finding` (with `context` enriched), it asks Claude
for a typed `Triage` verdict: true/false positive, re-rated severity,
exploitability reasoning, and a concrete fix.

The point of doing this generically: a security engineer's most expensive,
least-scalable activity is triaging a flood of scanner findings. The tool finds
*candidates*; this layer applies the judgment that decides which ones matter.
"""

from __future__ import annotations

from aug.client import AugClient
from aug.models import Finding, Triage

_PROMPT = """Triage this security finding.

Tool: {tool}
Rule: {rule_id}
Title: {title}
Tool-assigned severity: {severity}
Location: {location}

Description:
{description}

Evidence / context:
```
{context}
```

Decide whether this is a true positive, false positive, or needs human review.
Re-rate severity based on actual reachability and exposure shown in the \
evidence — not the tool's static rating. Explain your reasoning, note \
exploitability, and propose a concrete fix."""


def triage_finding(client: AugClient, finding: Finding, *, fast: bool = False) -> Triage:
    prompt = _PROMPT.format(
        tool=finding.tool,
        rule_id=finding.rule_id,
        title=finding.title,
        severity=finding.severity.value,
        location=finding.location,
        description=finding.description or "(none)",
        context=finding.context or "(no surrounding context was provided)",
    )
    return client.reason(prompt, Triage, fast=fast)


def triage_all(
    client: AugClient, findings: list[Finding], *, fast: bool = False
) -> list[tuple[Finding, Triage]]:
    """Triage a batch. Sequential and simple by design — swap in batching or
    the Message Batches API once you've measured your volume."""
    return [(f, triage_finding(client, f, fast=fast)) for f in findings]

"""Synthesize default-deny microsegmentation from observed traffic.

Usage:
    python microseg.py sample_flows.json --out scratch/policies/

The split that makes this trustworthy:
  - DETERMINISTIC: aggregate observed flows into per-destination allow
    candidates (which sources, ports, methods actually talk to each service).
    No model needed to know what was observed.
  - AI JUDGMENT: review the candidates for flows that look like they shouldn't
    be allow-listed (a service reaching the cloud metadata endpoint, an
    analytics job touching the prod database), then generate clean Istio
    AuthorizationPolicy YAML for the legitimate set with an explanation per rule.
  - GATE: everything is emitted with the istio.io/dry-run annotation and a
    REVIEW banner. A policy synthesized from observed traffic can lock out
    legitimate-but-rare flows, so it ships in audit mode for human sign-off
    before enforcement.

Input is a JSON list of observed flows (see sample_flows.json). In a real
deployment you'd feed mesh telemetry, VPC flow logs, or Zeek conn.log mapped
from IPs to workload identities — see module 05 for producing that.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft, Severity  # noqa: E402


# --- Input + aggregation (deterministic) -----------------------------------

class Flow(BaseModel):
    source: str = Field(description="Source workload identity (not an IP).")
    dest: str = Field(description="Destination workload identity.")
    port: int
    protocol: str = "tcp"
    method: str = ""   # HTTP method if known
    path: str = ""     # HTTP path if known
    count: int = 1     # how many times this flow was observed


def aggregate(flows: list[Flow]) -> list[dict]:
    """Collapse raw flows into one allow-candidate per destination service."""
    by_dest: dict[str, dict] = {}
    for f in flows:
        c = by_dest.setdefault(
            f.dest,
            {"dest": f.dest, "sources": set(), "ports": set(),
             "methods": set(), "paths": set(), "total": 0},
        )
        c["sources"].add(f.source)
        c["ports"].add(f.port)
        if f.method:
            c["methods"].add(f.method)
        if f.path:
            c["paths"].add(f.path)
        c["total"] += f.count
    # JSON-serializable, deterministic ordering
    return [
        {
            "dest": c["dest"],
            "sources": sorted(c["sources"]),
            "ports": sorted(c["ports"]),
            "methods": sorted(c["methods"]),
            "paths": sorted(c["paths"]),
            "total_flows": c["total"],
        }
        for c in sorted(by_dest.values(), key=lambda x: x["dest"])
    ]


# --- AI judgment result (structured output) --------------------------------

class FlowAnomaly(BaseModel):
    flow: str = Field(description="The suspicious flow, e.g. 'payments -> 169.254.169.254:80'.")
    reason: str = Field(description="Why it looks like it shouldn't be allow-listed.")
    severity: Severity


class MicrosegPlan(BaseModel):
    summary: str = Field(description="One-paragraph overview of the segmentation posture.")
    anomalies: list[FlowAnomaly] = Field(
        description="Observed flows that should be investigated, NOT silently allow-listed."
    )
    policies: list[PolicyDraft] = Field(
        description="One Istio AuthorizationPolicy per destination for the legitimate flows, "
        "plus a namespace default-deny. language='istio'."
    )


_PROMPT = """You are designing zero-trust microsegmentation from OBSERVED \
service-to-service traffic. Below are allow-candidates: for each destination \
service, the sources/ports/methods that were actually seen talking to it.

Two jobs:
1. ANOMALIES: flag any observed flow that looks like it should NOT be \
allow-listed even though it occurred — e.g. a workload reaching the cloud \
metadata endpoint (169.254.169.254), a non-prod/analytics identity touching a \
production datastore, egress to the internet, or an unusual port. These are \
candidate incidents, not policy.
2. POLICIES: for the LEGITIMATE flows only, generate one Istio \
AuthorizationPolicy (action: ALLOW) per destination service, keyed on the \
SOURCE WORKLOAD IDENTITY (SPIFFE principal cluster.local/ns/<ns>/sa/<svc>), \
restricted to the observed ports/methods/paths. Also include one namespace-wide \
default-deny AuthorizationPolicy (empty rules = deny all). Put the rendered YAML \
in each PolicyDraft.policy, set language='istio', and add the \
`istio.io/dry-run: "true"` annotation so it ships in audit mode. Do NOT create \
allow rules for any flow you flagged as an anomaly.

Assume namespace 'prod' unless a name implies otherwise. Explain each policy's \
intent and give allow/deny test_cases to verify.

Allow-candidates (from observed traffic):
```json
{candidates}
```"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("flows_json", help="JSON list of observed flows")
    ap.add_argument("--out", default="scratch/microseg", help="Where to write policy YAML")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()

    raw = json.loads(Path(args.flows_json).read_text())
    flows = [Flow(**r) for r in raw]
    candidates = aggregate(flows)
    print(f"Observed {len(flows)} flows across {len(candidates)} destination services.\n")

    client = AugClient()
    plan: MicrosegPlan = client.reason(
        _PROMPT.format(candidates=json.dumps(candidates, indent=2)),
        MicrosegPlan,
        max_tokens=12000,
        fast=args.fast,
    )

    print(plan.summary, "\n")

    if plan.anomalies:
        print("ANOMALIES — investigate, do NOT allow-list:")
        for a in plan.anomalies:
            print(f"  [{a.severity.value}] {a.flow}\n      {a.reason}")
        print()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, pol in enumerate(plan.policies):
        name = f"{i:02d}-policy.yaml"
        (out / name).write_text(pol.policy + "\n")
        print(f"wrote {out / name}  — {pol.intent}")

    print(
        "\n*** REVIEW BEFORE ENFORCING ***\n"
        "Policies are written with istio.io/dry-run: \"true\". Apply them in "
        "dry-run, watch the audit logs for legitimate flows you'd block, then "
        "flip to enforcement only after human sign-off."
    )


if __name__ == "__main__":
    main()

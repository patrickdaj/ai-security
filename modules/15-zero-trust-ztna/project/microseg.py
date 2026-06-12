"""STUB — synthesize default-deny microsegmentation from observed traffic.

Build this; the worked answer is in ../reference/microseg.py. Run against
sample_flows.json. The deterministic aggregation is given (that's the easy half);
your job is the AI half: flag anomalies and generate the Istio policies.

    python microseg.py sample_flows.json --out scratch/microseg
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft, Severity  # noqa: E402


class Flow(BaseModel):
    source: str
    dest: str
    port: int
    protocol: str = "tcp"
    method: str = ""
    path: str = ""
    count: int = 1


def aggregate(flows: list[Flow]) -> list[dict]:
    """GIVEN: collapse raw flows into one allow-candidate per destination."""
    by_dest: dict[str, dict] = {}
    for f in flows:
        c = by_dest.setdefault(f.dest, {"dest": f.dest, "sources": set(), "ports": set(), "total": 0})
        c["sources"].add(f.source)
        c["ports"].add(f.port)
        c["total"] += f.count
    return [
        {"dest": c["dest"], "sources": sorted(c["sources"]), "ports": sorted(c["ports"]),
         "total_flows": c["total"]}
        for c in sorted(by_dest.values(), key=lambda x: x["dest"])
    ]


class MicrosegPlan(BaseModel):
    summary: str
    # TODO: add `anomalies` (flows that shouldn't be allow-listed) and
    # `policies: list[PolicyDraft]` (one Istio AuthorizationPolicy per dest +
    # a default-deny). See the reference for the exact shape.


def synthesize(client: AugClient, candidates: list[dict]) -> MicrosegPlan:
    # TODO: write the prompt that asks the model to (1) flag anomalies like a
    # workload reaching 169.254.169.254 or analytics touching prod DB, and
    # (2) emit Istio policies (action ALLOW, SPIFFE principals, dry-run
    # annotation) for the legitimate flows only. Then: client.reason(prompt, MicrosegPlan)
    raise NotImplementedError("Build the anomaly-flagging + policy-generation prompt.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("flows_json")
    ap.add_argument("--out", default="scratch/microseg")
    args = ap.parse_args()
    flows = [Flow(**r) for r in json.loads(Path(args.flows_json).read_text())]
    candidates = aggregate(flows)
    plan = synthesize(AugClient(), candidates)
    print(plan.summary)  # TODO: write policies to --out, print anomalies + REVIEW gate


if __name__ == "__main__":
    main()

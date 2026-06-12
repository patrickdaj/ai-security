"""STUB — cloud purple-team loop. Worked answer in ../reference/purple_loop.py.

Build the loop: plan TTPs -> detonate (gated) -> check detection -> synthesize
the missing Sigma rule. The authorization gate is given (don't weaken it); the
AI steps are yours.

    python purple_loop.py --env-desc env.txt --events sample_cloudtrail.json
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft, Severity  # noqa: E402


class TechniqueChoice(BaseModel):
    id: str
    tactic: str
    relevance: Severity
    rationale: str


class EmulationPlan(BaseModel):
    techniques: list[TechniqueChoice]


def plan_emulation(client: AugClient, env_desc: str, k: int) -> EmulationPlan:
    # TODO: prompt the model to pick up to k relevant Stratus technique ids for
    # this environment, then: return client.reason(prompt, EmulationPlan)
    raise NotImplementedError("Build the technique-selection prompt.")


def check_detection(client: AugClient, ttp: str, events: str):
    # TODO: define a DetectionCheck schema (detected: bool, gap: str, ...) and
    # ask the model whether the events would be caught. Return it.
    raise NotImplementedError("Build the detection-check step.")


def synthesize_detection(client: AugClient, ttp: str, gap: str) -> PolicyDraft:
    # TODO: ask for a tight Sigma rule (PolicyDraft, language='sigma') for the gap.
    raise NotImplementedError("Build the Sigma synthesis step.")


def authorize_live(args) -> bool:
    """GIVEN — do not weaken. Live detonation needs multi-signal authorization."""
    if not args.live:
        return False
    if not args.i_am_authorized or os.getenv("STRATUS_ALLOW") != "1":
        sys.exit("REFUSED: --live needs --i-am-authorized AND STRATUS_ALLOW=1.")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-desc", required=True)
    ap.add_argument("--events")
    ap.add_argument("--max-techniques", type=int, default=5)
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--i-am-authorized", action="store_true")
    args = ap.parse_args()

    authorize_live(args)
    client = AugClient()
    env = Path(args.env_desc).read_text()
    events = Path(args.events).read_text() if args.events else "[]"
    plan = plan_emulation(client, env, args.max_techniques)
    for t in plan.techniques:
        print(t.id)
        # TODO: detonate (dry-run unless live), check_detection, and on a gap
        # synthesize_detection + write the rule. See the reference.


if __name__ == "__main__":
    main()

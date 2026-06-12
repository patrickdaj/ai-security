"""Cloud purple-team loop: emulate ATT&CK TTPs, check detection, close the gap.

The loop:
    plan      -> AI picks Stratus Red Team techniques relevant to the environment
    detonate  -> run the technique (Stratus) against an AUTHORIZED account
    check     -> AI decides whether your telemetry/detections caught it
    synthesize-> for gaps, AI drafts the missing Sigma detection
    report    -> a purple-team summary

This ties modules 09 (detection), 11 (cloud identity), and 13/15 (runtime/ztna)
together: offense reveals the gap, AI writes the detection that closes it.

GATE — read this:
  Detonation runs *real* attack techniques against a *real* cloud account. It is
  destructive and outward-facing. It is OFF by default. `--live` is refused
  unless you also pass `--i-am-authorized` AND set STRATUS_ALLOW=1, confirming
  this is an account you own or are explicitly authorized to test. Without
  `--live` the loop runs in dry-run: it prints the commands it WOULD run and
  reasons over an events file you supply.

Usage:
    # Dry-run (safe): plan + reason over recorded events, synthesize detections
    python purple_loop.py --env-desc env.txt --events sample_cloudtrail.json

    # Live (authorized accounts only)
    STRATUS_ALLOW=1 python purple_loop.py --env-desc env.txt --live --i-am-authorized
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aug import AugClient, PolicyDraft, Severity  # noqa: E402


# --- Schemas (structured outputs) ------------------------------------------

class TechniqueChoice(BaseModel):
    id: str = Field(description="Stratus Red Team technique id, e.g. 'aws.persistence.iam-create-admin-user'.")
    tactic: str = Field(description="ATT&CK tactic, e.g. 'Persistence'.")
    relevance: Severity = Field(description="How relevant to the described environment.")
    rationale: str


class EmulationPlan(BaseModel):
    techniques: list[TechniqueChoice]
    notes: str = ""


class DetectionCheck(BaseModel):
    detected: bool = Field(description="Would the existing telemetry/detections catch this?")
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str = Field(description="Which events/rules support the verdict.")
    gap: str = Field(default="", description="If undetected: what a detection would need to key on.")


# --- AI steps ---------------------------------------------------------------

def plan_emulation(client: AugClient, env_desc: str, k: int) -> EmulationPlan:
    prompt = (
        f"You are planning an authorized cloud purple-team exercise using Stratus "
        f"Red Team. Given this environment, select up to {k} Stratus techniques "
        f"that are most relevant to emulate (real Stratus technique ids), ordered "
        f"by relevance. Favor techniques that exercise the environment's actual "
        f"exposure.\n\nEnvironment:\n{env_desc}"
    )
    return client.reason(prompt, EmulationPlan)


def check_detection(client: AugClient, ttp: str, events: str, detections: str) -> DetectionCheck:
    prompt = (
        f"Technique emulated: {ttp}\n\n"
        f"Activity captured afterward (CloudTrail / runtime events):\n```json\n{events}\n```\n\n"
        f"Existing detections in place:\n{detections or '(none provided)'}\n\n"
        f"Decide whether this activity WOULD be detected by the existing detections. "
        f"Ground the verdict in the events. If undetected, describe precisely what a "
        f"detection would need to key on."
    )
    return client.reason(prompt, DetectionCheck)


def synthesize_detection(client: AugClient, ttp: str, gap: str, events: str) -> PolicyDraft:
    prompt = (
        f"Write a Sigma detection rule that catches technique {ttp}.\n"
        f"Detection gap to close: {gap}\n\n"
        f"Representative activity it must match:\n```json\n{events}\n```\n\n"
        f"Return a PolicyDraft with language='sigma', a tight detection (avoid "
        f"overbroad selections that bury the SOC in false positives), the rendered "
        f"rule in `policy`, and allow/deny test_cases."
    )
    return client.reason(prompt, PolicyDraft)


# --- Detonation (gated, real cloud I/O) ------------------------------------

def detonate(ttp: str, live: bool) -> None:
    """Run a Stratus technique. Real attack against a real account when live."""
    warmup = ["stratus", "warmup", ttp]
    fire = ["stratus", "detonate", ttp]
    cleanup = ["stratus", "cleanup", ttp]
    if not live:
        print(f"  [dry-run] would run: {' '.join(warmup)} && {' '.join(fire)}")
        print(f"  [dry-run] cleanup:   {' '.join(cleanup)}")
        return
    print(f"  detonating {ttp} ...")
    subprocess.run(warmup, check=True)
    try:
        subprocess.run(fire, check=True)
    finally:
        # Always attempt cleanup so the exercise leaves no persistent attacker state.
        subprocess.run(cleanup, check=False)


def authorize_live(args) -> bool:
    """Hard gate. Live detonation requires explicit, multi-signal authorization."""
    if not args.live:
        return False
    if not args.i_am_authorized or os.getenv("STRATUS_ALLOW") != "1":
        sys.exit(
            "REFUSED: --live detonates real attack techniques against a real "
            "cloud account. Pass --i-am-authorized AND set STRATUS_ALLOW=1 only "
            "for an account you own or are explicitly authorized to test."
        )
    return True


# --- Orchestration ----------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-desc", required=True, help="File describing the target environment")
    ap.add_argument("--events", help="JSON events file to reason over in dry-run")
    ap.add_argument("--detections", help="File listing existing detections (optional)")
    ap.add_argument("--max-techniques", type=int, default=5)
    ap.add_argument("--out", default="scratch/purple", help="Where to write synthesized rules")
    ap.add_argument("--live", action="store_true", help="Actually detonate (gated)")
    ap.add_argument("--i-am-authorized", action="store_true")
    args = ap.parse_args()

    live = authorize_live(args)
    env_desc = Path(args.env_desc).read_text()
    events = Path(args.events).read_text() if args.events else "[]"
    detections = Path(args.detections).read_text() if args.detections else ""

    client = AugClient()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print("Planning emulation...\n")
    plan = plan_emulation(client, env_desc, args.max_techniques)
    print(plan.notes, "\n" if plan.notes else "")

    gaps = 0
    for t in plan.techniques:
        print(f"=== {t.id}  [{t.tactic}, relevance {t.relevance.value}]")
        print(f"    {t.rationale}")
        detonate(t.id, live)
        check = check_detection(client, t.id, events, detections)
        status = "DETECTED" if check.detected else "MISSED"
        print(f"    detection: {status} (conf {check.confidence:.2f}) — {check.evidence}")
        if not check.detected:
            gaps += 1
            rule = synthesize_detection(client, t.id, check.gap, events)
            path = out / f"{t.id.replace('.', '_')}.sigma.yml"
            path.write_text(rule.policy + "\n")
            print(f"    -> gap. wrote detection: {path}")
        print()

    print(f"Done. {len(plan.techniques)} techniques, {gaps} detection gap(s) closed.")
    if not live:
        print("(dry-run — no techniques were detonated; pass --live for an authorized account)")


if __name__ == "__main__":
    main()

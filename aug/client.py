"""AugClient — an opinionated wrapper over the Anthropic SDK.

Why wrap it: every module wants the same thing — send some normalized security
context to Claude and get back a *typed* answer. This centralizes the model
defaults, the structured-output plumbing, and the "keep reasoning grounded in
the provided evidence" system prompt so each module's augmentation stays small.

Models (see .env.example):
  - default  claude-opus-4-8   most capable; use for judgment-heavy triage
  - fast     claude-haiku-4-5  cheap; use for high-volume classification
"""

from __future__ import annotations

import os
from typing import TypeVar

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

DEFAULT_MODEL = os.getenv("AUG_MODEL", "claude-opus-4-8")
FAST_MODEL = os.getenv("AUG_FAST_MODEL", "claude-haiku-4-5")

T = TypeVar("T", bound=BaseModel)

# The reasoning layer must stay grounded in evidence the tool gathered, and must
# never fabricate exploitability. This is the spine of trustworthy AppSec
# automation: opinions are fine, invented facts are not.
SYSTEM = """You are a senior security engineer acting as a judgment layer on top \
of deterministic security tooling. You receive normalized findings or telemetry \
plus surrounding evidence (code, packets, advisories, diffs).

Rules:
- Ground every conclusion in the evidence provided. If the evidence is \
insufficient to decide, say so and return a needs_review / lower-confidence \
verdict rather than guessing.
- Do not invent exploitability. Reason about reachability and exposure only \
from what you can see.
- Prefer concrete, minimal remediations (a diff or exact code) over generic \
advice.
- Calibrate confidence honestly. Reserve high confidence for cases the \
evidence clearly supports."""


class AugClient:
    """Thin client returning typed results via structured outputs."""

    def __init__(self, model: str | None = None, fast_model: str | None = None):
        self._client = anthropic.Anthropic()
        self.model = model or DEFAULT_MODEL
        self.fast_model = fast_model or FAST_MODEL

    def reason(
        self,
        prompt: str,
        schema: type[T],
        *,
        fast: bool = False,
        system: str | None = None,
        max_tokens: int = 8000,
    ) -> T:
        """Send `prompt` to Claude and parse the reply into `schema`.

        Uses structured outputs so the result is a validated Pydantic instance,
        not text you have to scrape. Adaptive thinking is on so the model can
        reason about reachability before committing to a verdict.
        """
        response = self._client.messages.parse(
            model=self.fast_model if fast else self.model,
            max_tokens=max_tokens,
            system=system or SYSTEM,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
            output_format=schema,
        )
        if response.parsed_output is None:
            raise RuntimeError(
                f"Model did not return a valid {schema.__name__} "
                f"(stop_reason={response.stop_reason})."
            )
        return response.parsed_output

    def text(self, prompt: str, *, fast: bool = False, max_tokens: int = 4000) -> str:
        """Plain-text reply, for when you want prose (a narrative, a summary)."""
        response = self._client.messages.create(
            model=self.fast_model if fast else self.model,
            max_tokens=max_tokens,
            system=SYSTEM,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in response.content if b.type == "text")

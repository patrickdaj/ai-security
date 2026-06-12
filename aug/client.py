"""AugClient — the single, provider-agnostic surface the whole curriculum uses.

Every module wants the same thing: send normalized security context to a model
and get back a *typed* answer. AugClient centralizes that, the grounding system
prompt, and the choice of backend, so each module's augmentation stays small.

Backends (see aug/backends.py):
  - anthropic (default)  Claude via the Anthropic SDK. What the modules are
                         tuned for; sharpest judgments, reliable structured
                         outputs, adaptive thinking.
  - ollama               A local model via Ollama. Opt in for data residency,
                         offline work, or cost — at some quality cost.

Select with AUG_BACKEND (anthropic|ollama). Models (see .env.example):
  anthropic: AUG_MODEL=claude-opus-4-8   AUG_FAST_MODEL=claude-haiku-4-5
  ollama:    AUG_OLLAMA_MODEL=llama3.1    AUG_OLLAMA_FAST_MODEL=<same by default>
"""

from __future__ import annotations

import os
from typing import TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel

from aug.backends import AnthropicBackend, OllamaBackend

load_dotenv()

BACKEND = os.getenv("AUG_BACKEND", "anthropic").lower()
DEFAULT_MODEL = os.getenv("AUG_MODEL", "claude-opus-4-8")
FAST_MODEL = os.getenv("AUG_FAST_MODEL", "claude-haiku-4-5")
OLLAMA_MODEL = os.getenv("AUG_OLLAMA_MODEL", "llama3.1")
OLLAMA_FAST_MODEL = os.getenv("AUG_OLLAMA_FAST_MODEL", OLLAMA_MODEL)

T = TypeVar("T", bound=BaseModel)

# The reasoning layer must stay grounded in evidence the tool gathered, and must
# never fabricate exploitability. This is the spine of trustworthy AppSec
# automation: opinions are fine, invented facts are not. Used by both backends.
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
    """Provider-agnostic client returning typed results via structured outputs."""

    def __init__(
        self,
        backend: str | None = None,
        model: str | None = None,
        fast_model: str | None = None,
    ):
        name = (backend or BACKEND).lower()
        if name == "ollama":
            self.backend = "ollama"
            self.model = model or OLLAMA_MODEL
            self.fast_model = fast_model or OLLAMA_FAST_MODEL
            self._impl = OllamaBackend(self.model, self.fast_model)
        elif name == "anthropic":
            self.backend = "anthropic"
            self.model = model or DEFAULT_MODEL
            self.fast_model = fast_model or FAST_MODEL
            self._impl = AnthropicBackend(self.model, self.fast_model)
        else:
            raise ValueError(
                f"Unknown AUG_BACKEND '{name}'. Use 'anthropic' or 'ollama'."
            )

    def reason(
        self,
        prompt: str,
        schema: type[T],
        *,
        fast: bool = False,
        system: str | None = None,
        max_tokens: int = 8000,
    ) -> T:
        """Send `prompt` to the model and parse the reply into `schema`.

        Returns a validated Pydantic instance, not text you have to scrape — the
        typed contract that lets you trust a model in an automated pipeline.
        """
        return self._impl.reason(
            prompt, schema, system=system or SYSTEM, fast=fast, max_tokens=max_tokens
        )

    def text(self, prompt: str, *, fast: bool = False, max_tokens: int = 4000) -> str:
        """Plain-text reply, for when you want prose (a narrative, a summary)."""
        return self._impl.text(prompt, system=SYSTEM, fast=fast, max_tokens=max_tokens)

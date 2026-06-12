"""Pluggable reasoning backends.

The curriculum is Claude-first: the Anthropic backend is the default and the one
the modules are tuned for (adaptive thinking + structured outputs give the
sharpest, most reliably-typed judgments). But security work has a real
data-residency dimension — you may not want to send proprietary code, secret
context, or a cloud IAM graph to any external API. So we also ship a local
**Ollama** backend behind the exact same interface.

Both backends:
  - take the same grounding `system` prompt,
  - return a validated Pydantic instance from `reason()` (structured outputs),
  - return plain text from `text()`.

Provider SDKs are imported lazily inside each backend's constructor, so
`import aug` works whether or not anthropic/ollama are installed.
"""

from __future__ import annotations

import os
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class AnthropicBackend:
    """Claude via the Anthropic SDK. The default. Uses adaptive thinking so the
    model can reason about reachability before committing, and structured
    outputs so the reply is a typed Pydantic instance."""

    def __init__(self, model: str, fast_model: str):
        import anthropic  # lazy: only needed when this backend is selected

        self._client = anthropic.Anthropic()
        self.model = model
        self.fast_model = fast_model

    def reason(
        self, prompt: str, schema: type[T], *, system: str, fast: bool, max_tokens: int
    ) -> T:
        response = self._client.messages.parse(
            model=self.fast_model if fast else self.model,
            max_tokens=max_tokens,
            system=system,
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

    def text(self, prompt: str, *, system: str, fast: bool, max_tokens: int) -> str:
        response = self._client.messages.create(
            model=self.fast_model if fast else self.model,
            max_tokens=max_tokens,
            system=system,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in response.content if b.type == "text")


class OllamaBackend:
    """A local model served by Ollama. Opt in with AUG_BACKEND=ollama.

    Structured outputs use Ollama's `format` parameter with the schema's JSON
    Schema, then validate the returned JSON against the Pydantic model. Pick a
    model that follows JSON/tool instructions well (e.g. llama3.1, qwen2.5,
    mistral-nemo); smaller models will produce weaker security judgments and may
    fail schema validation more often — that's the quality/privacy tradeoff.

    Honors OLLAMA_HOST (or AUG_OLLAMA_HOST) for a remote daemon. Set
    AUG_OLLAMA_THINK=1 to enable thinking on models that support it (e.g.
    qwen3, deepseek-r1).
    """

    def __init__(self, model: str, fast_model: str):
        try:
            import ollama  # lazy: only needed when this backend is selected
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "The Ollama backend needs the optional dependency. "
                "Install it with: pip install -e '.[local]'"
            ) from e

        self._client = ollama.Client(host=os.getenv("AUG_OLLAMA_HOST"))
        self.model = model
        self.fast_model = fast_model
        self._think = os.getenv("AUG_OLLAMA_THINK", "").lower() in ("1", "true", "yes")

    def _chat(self, prompt: str, system: str, fast: bool, max_tokens: int, fmt=None):
        kwargs: dict = {
            "model": self.fast_model if fast else self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "options": {"num_predict": max_tokens},
        }
        if fmt is not None:
            kwargs["format"] = fmt
        if self._think:
            kwargs["think"] = True
        return self._client.chat(**kwargs)

    def reason(
        self, prompt: str, schema: type[T], *, system: str, fast: bool, max_tokens: int
    ) -> T:
        response = self._chat(
            prompt, system, fast, max_tokens, fmt=schema.model_json_schema()
        )
        content = response.message.content or ""
        try:
            return schema.model_validate_json(content)
        except Exception as e:  # noqa: BLE001 - surface as one clear error
            raise RuntimeError(
                f"Local model did not return valid {schema.__name__}. "
                f"Try a stronger model (AUG_OLLAMA_MODEL) or inspect the raw output:\n"
                f"{content[:500]}"
            ) from e

    def text(self, prompt: str, *, system: str, fast: bool, max_tokens: int) -> str:
        response = self._chat(prompt, system, fast, max_tokens)
        return response.message.content or ""

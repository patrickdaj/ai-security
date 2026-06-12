"""aug — the AI-augmentation layer for the security curriculum.

This package is the shared substrate every module builds on. It gives you:

- `aug.client.AugClient`   a thin, opinionated wrapper over the Anthropic SDK
                           that returns *typed* results via structured outputs.
- `aug.models`             common schemas (Finding, Triage, Severity, ...) so
                           every tool's output normalizes to one shape.
- `aug.triage`            a generic, tool-agnostic finding-triage engine.

The design goal: the LLM is a judgment layer bolted onto deterministic tools,
not a replacement. Keep parsing deterministic, keep the model's job to
*reason* over normalized inputs, and keep a human gate on anything destructive.
"""

from aug.client import AugClient
from aug.models import Finding, Severity, Triage, TriageVerdict

__all__ = ["AugClient", "Finding", "Severity", "Triage", "TriageVerdict"]

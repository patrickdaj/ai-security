# Module 10 — LLM / ML Security

The meta-module: securing AI systems themselves. Now that you've used AI to
augment security tools, you flip it around and learn to *attack and defend*
LLM-powered applications — prompt injection, jailbreaks, data exfiltration,
unsafe tool use — using the emerging open-source AI red-team toolchain.

## Tools you tour

- **garak** — an LLM vulnerability scanner; runs probes (jailbreaks, prompt
  leaking, toxicity, package hallucination) against a model or app.
- **PyRIT** — Microsoft's Python Risk Identification Toolkit for generative AI;
  orchestrates automated red-teaming with attack strategies and scorers.
- **promptfoo** — eval + red-team harness; great for regression-testing
  guardrails and running adversarial test suites in CI.
- **Rebuff** — a prompt-injection *defense* layer (heuristics, canaries, an
  LLM-based detector) — the thing you build against.

### Tour tasks

```bash
garak --model_type openai --model_name <your-app-proxy> --probes promptinject
promptfoo redteam run            # after `promptfoo redteam init`
```

Run garak against a small LLM app you stand up (a RAG bot, or a tool-using
agent). Watch which probes land. Those are your real vulnerabilities.

## AI augmentation: prompt-injection red-team + guardrail harness

This module's "augmentation" is dual-use and deliberate: you use AI both as the
**attacker** (generating adversarial inputs) and the **defender** (classifying
whether a response was successfully manipulated).

Two builds:

1. **Red-team generator.** Generate a corpus of prompt-injection / jailbreak
   payloads targeting a described system, run them through your app, and use a
   model-based scorer to decide which succeeded. (Authorized targets only — your
   own app.)
2. **Guardrail harness.** Wrap your app with input/output filters (à la Rebuff:
   canary tokens, an injection detector, output policy checks) and use promptfoo
   to regression-test that known attacks stay blocked as you iterate.

Define `InjectionAttempt { payload, technique, succeeded, evidence }` and a
`GuardrailVerdict`. Keep the attacker and scorer as *separate* model calls so the
scorer isn't biased by having authored the attack.

> Ethics gate: everything here targets systems you own or are authorized to
> test. The goal is hardening your own AI apps, not attacking others'.

## Exercises

1. Build a tiny vulnerable RAG app (a system prompt with a "secret"), then use
   the generator to extract the secret and score the extraction.
2. Add a Rebuff-style guardrail and re-run; measure the drop in successful
   injections.
3. Wire the attack corpus into promptfoo so guardrail regressions fail CI.
4. Connect this back to module 09: emit a detection (a log signature) for
   successful injection attempts.

## Done when

- You can red-team your own LLM app end-to-end (generate → run → score), stand up
  a guardrail that measurably blocks the attacks, and keep it from regressing in
  CI.

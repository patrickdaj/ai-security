# Module 00 — Foundations & Lab

Before touring tools, you set up two things: a **safe lab** to attack, and the
**`aug` augmentation library** that every later module wires into. You also
ground yourself in the mental model that makes the rest of the curriculum
cohere: tools generate candidates; judgment decides what matters; AI scales the
judgment.

## Learning objectives

- Stand up an isolated lab of intentionally-vulnerable targets.
- Understand the augmentation pattern (normalize → enrich → reason → gate).
- Get the `aug` library working end-to-end against a real Claude model.
- Internalize *structured outputs* as the contract between deterministic tools
  and the reasoning layer.

## Concepts

### Threat modeling in one page

Every engagement starts by answering: what are we protecting, from whom, and
where are the trust boundaries? Skim STRIDE and attack trees. You don't need
ceremony — you need the habit of asking "where does untrusted input cross into
trusted code?" because that question is exactly what you'll later ask Claude to
reason about for each finding.

### The augmentation pattern

```
normalize  ──►  enrich  ──►  reason (structured)  ──►  gate
   │              │              │                       │
 tool output   add the       Claude returns a         no auto-action on
 → Finding     code/packet   typed Triage, not        anything irreversible;
   schema      /advisory     prose                     surface confidence
```

This is implemented once in [`aug/`](../../aug). Read these three files now:

- `aug/models.py` — the normalized `Finding` and `Triage` schemas.
- `aug/client.py` — `AugClient.reason()` returns typed Pydantic via structured
  outputs, with a grounding system prompt.
- `aug/triage.py` — the generic triage engine modules 01–04 reuse.

### Why structured outputs matter here

If the model replies with prose, you're back to scraping text. By forcing the
reply into a `Triage` schema, the verdict becomes sortable, filterable,
confidence-gatable, and pipe-able into a tracker. That typed contract is what
lets you trust an LLM in an automated security pipeline.

## Lab

```bash
make lab-up      # DVWA, Juice Shop, (your vuln-app) on an isolated network
```

See [`labs/README.md`](../../labs/README.md). **Localhost only. Authorized
targets only.**

## Project: get the AI layer running

```bash
python -m venv .venv && source .venv/bin/activate
make setup                 # pip install -e ".[dev]"
cp .env.example .env       # add your ANTHROPIC_API_KEY
make smoke                 # python -m aug.smoke
```

Success looks like: the SQL-injection example comes back as a high-severity
`true_positive` with a parameterized-query fix and calibrated confidence.

## Exercises

1. Add a `Finding.from_dict` classmethod and a tiny adapter that loads a hand-
   written finding from JSON, then triage it.
2. Make the smoke example a *false* positive (e.g. the "user input" is actually
   a hardcoded constant) and confirm the verdict flips and confidence drops.
3. Swap `AUG_MODEL` to `claude-sonnet-4-6` and compare triage quality vs. cost
   on a batch of 10 findings.

## Done when

- `make smoke` returns a sensible typed `Triage`.
- You can articulate, in two sentences, why the LLM here is a *layer on top of*
  tools rather than a replacement for them.

# Module 00 — Foundations & Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


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

### Choosing a backend

`AugClient` runs on Claude (default) or a local Ollama model — same schemas,
same code. Claude is what the modules are tuned for; reach for Ollama when data
residency, offline work, or cost matters (see the root README's *Backends*
section). To try local:

```bash
pip install -e ".[local]" && ollama pull llama3.1
AUG_BACKEND=ollama python -m aug.smoke
```

## Exercises

1. Add a `Finding.from_dict` classmethod and a tiny adapter that loads a hand-
   written finding from JSON, then triage it.
2. Make the smoke example a *false* positive (e.g. the "user input" is actually
   a hardcoded constant) and confirm the verdict flips and confidence drops.
3. Swap `AUG_MODEL` to `claude-sonnet-4-6` and compare triage quality vs. cost
   on a batch of 10 findings.
4. Run the same batch under `AUG_BACKEND=ollama` with a local model and compare
   against Claude — where does the local model's reasoning hold up, and where
   does it miss reachability nuance or fail schema validation? This calibrates
   when the privacy/cost tradeoff is worth it.

## Done when

- `make smoke` returns a sensible typed `Triage`.
- You can articulate, in two sentences, why the LLM here is a *layer on top of*
  tools rather than a replacement for them.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- [DVWA](https://github.com/digininja/DVWA)
- [Anthropic API docs (structured outputs, tool use)](https://platform.claude.com/docs)

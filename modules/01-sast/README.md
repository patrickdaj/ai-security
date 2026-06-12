# Module 01 — Static Analysis (SAST)

Static analysis tools read code without running it and flag patterns that *may*
be bugs. Their fatal weakness is the false-positive flood: they over-report
because they can't reason about reachability or intent. This is the canonical
place to bolt on AI judgment.

## Tools you tour

- **Semgrep** — pattern-based, language-aware grep with a huge rule registry.
  Start here; rules are readable and the output is clean JSON/SARIF.
- **CodeQL** — treats code as a database you query with a real query language;
  models data flow and taint. Heavier, far more powerful.
- **Bandit** — Python-specific, fast, noisy; great for generating a finding pile
  to triage.

### Tour tasks

```bash
# Semgrep against the vuln-app (or any repo)
semgrep --config=auto --json -o scratch/semgrep.json labs/vuln-app/

# Bandit over a Python target
bandit -r labs/vuln-app/ -f json -o scratch/bandit.json
```

Read the JSON. Notice: each finding has a rule, a location, and a snippet — but
no notion of whether the tainted input is actually reachable from an attacker.
That missing reasoning is your augmentation's job.

## AI augmentation: auto-triage + fix-suggestion engine

Build a CLI that ingests Semgrep/Bandit JSON, normalizes each result into a
`Finding` (pulling the surrounding code into `.context`), runs it through the
shared triage engine, and emits a ranked, de-noised report with concrete fixes.

The skeleton lives in [`project/`](./project):

```bash
python modules/01-sast/project/triage_sast.py scratch/semgrep.json
```

Key idea: **enrichment is what makes the triage good.** A finding with just a
line number gives the model little to reason about. Pull ~15 lines around the
hit, and if you can, the function signature and the call sites, into `.context`.
The better the evidence, the sharper the false-positive culling.

## Exercises

1. Enrich findings with the *enclosing function* (use `tree-sitter` or a crude
   brace/indent scan) and measure the false-positive reduction vs. line-only
   context.
2. Add a `--min-confidence` gate so only high-confidence true positives become
   tickets, and route `needs_review` to a separate queue.
3. Have the model emit fixes as unified diffs and apply the high-confidence ones
   to a scratch branch automatically — but never to `main` (the gate).
4. Stretch: feed CodeQL's data-flow path into `.context` and see how much
   reachability reasoning improves.

## Done when

- You can take a raw Semgrep run and produce a triaged report where the noise is
  visibly reduced and each surviving finding has a concrete, code-level fix.
- You can explain which false positives the model caught and *why the evidence
  let it*.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Semgrep docs + writing rules](https://semgrep.dev/docs/writing-rules/overview)
- [CodeQL docs](https://codeql.github.com/docs/)
- [Bandit](https://bandit.readthedocs.io/)
- [OWASP Source Code Analysis Tools](https://owasp.org/www-community/Source_Code_Analysis_Tools)

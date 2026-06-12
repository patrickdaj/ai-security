# Module 02 — Secrets Detection

Secret scanners find high-entropy strings and known credential patterns in code
and git history. The problem: most hits are example keys, test fixtures, rotated
creds, or random base64 that *looks* like a secret. AI is excellent at the
classification call these tools can't make.

## Tools you tour

- **TruffleHog** — scans git history and live systems; can *verify* some secrets
  by calling the provider. Strong signal when verification succeeds.
- **Gitleaks** — fast regex/entropy scanner with a clean config model; great for
  CI gates and for generating a finding pile.

### Tour tasks

```bash
gitleaks detect --source . --report-format json --report-path scratch/gitleaks.json
trufflehog filesystem . --json > scratch/trufflehog.json
```

Look at the hits. Sort the real from the noise by hand first — that's the task
you're about to teach the model to do.

## AI augmentation: secret validator/classifier

Build a classifier that, for each hit, decides: live credential, test/example,
already-rotated, or false positive — and assigns a blast-radius estimate. Pull
the surrounding lines and the filename into `.context` (a key in
`tests/fixtures/` is almost certainly fake; one in `config/prod.py` is not).

Reuse the `aug` pattern, but define a `SecretVerdict` schema (don't shoehorn it
into the generic `Triage` — secrets have their own categories).

> **Never** send a *live* secret to any external service for "validation" via
> the LLM. The model classifies based on context and surrounding code; actual
> verification stays with TruffleHog's provider checks, which you trigger
> deterministically. This is a gate.

## Exercises

1. Define `SecretVerdict { kind, is_live_guess, blast_radius, rotate_now }` and
   classify a Gitleaks run.
2. Weight the decision by path: model the prior that `tests/`, `examples/`,
   `*.md` lower the live-secret probability.
3. Combine signals: if TruffleHog *verified* a secret, mark it live
   deterministically and use the model only for blast-radius narrative.

## Done when

- You can turn a noisy Gitleaks/TruffleHog run into a short list of
  rotate-now-with-blast-radius items, with the obvious fixtures filtered out —
  and your pipeline never exfiltrates a real secret to do it.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

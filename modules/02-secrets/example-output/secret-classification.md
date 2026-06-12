<!-- Example output — illustrative deliverable of module 02. -->

# Secret Classification — `vuln-app`

Gitleaks: 23 hits → classified. **2 rotate-now**, 21 noise.

| File:line | Rule | Kind | Live? | Blast | Action |
|-----------|------|------|-------|-------|--------|
| `config/settings.py:12` | aws-access-key | live | yes | high | **ROTATE NOW** — prod IAM key in committed config. |
| `deploy/.env:3` | generic-api-key | live | yes | medium | **ROTATE NOW** — Stripe key; scope is payments. |
| `tests/fixtures.py:5` | aws-access-key | test_or_example | no | info | none — fixture under `tests/`, value is `AKIAEXAMPLE`. |
| `README.md:88` | generic-api-key | test_or_example | no | info | none — documentation placeholder. |
| `app/cache.py:9` | hex-high-entropy | false_positive | no | info | none — a cache-key hash, not a credential. |

**Outcome:** 23 hits → 2 real, rotate-now items with blast radius; 21 fixtures
and false positives filtered. No secret value was sent to the model.

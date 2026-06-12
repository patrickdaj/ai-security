<!-- Example output — illustrative deliverable of module 12. -->

# CI/CD Pipeline Audit — `.github/workflows/`

zizmor: 6 findings → audited. 1 critical, 2 high.

## CRITICAL — secret exfiltration via `pull_request_target`
**File:** `.github/workflows/pr.yml` · risk: high
**Attack:** the workflow triggers on `pull_request_target` (runs with repo
secrets) but checks out `github.event.pull_request.head.sha` — attacker-
controlled fork code. A malicious PR runs arbitrary code with your secrets in
scope → full secret exfiltration.
```diff
-on: pull_request_target
+on: pull_request           # no secret access for fork PRs
 jobs:
   build:
     steps:
-      - uses: actions/checkout@v4
-        with:
-          ref: ${{ github.event.pull_request.head.sha }}
+      - uses: actions/checkout@v4   # default ref; no secret-scoped checkout of PR head
```

## HIGH — unpinned action + overbroad token
- `uses: some/action@main` → pin to a commit SHA.
- `permissions: write-all` → scope to `contents: read`.

**Outcome:** the real poisoned-pipeline path is explained and patched; the noise
is deprioritized.

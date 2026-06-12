# The Lab

Intentionally-vulnerable targets to practice against. **Run these only in the
isolated Docker network defined here. Never expose them to the internet, and
never point the curriculum's tools at anything you don't own.**

## Targets

| Service | Port | Use it for |
|---------|------|------------|
| DVWA (Damn Vulnerable Web App) | 8081 | SQLi, XSS, command injection — modules 01, 04 |
| OWASP Juice Shop | 3000 | Modern SPA bugs, API testing — module 04 |
| A deliberately vulnerable Python service | 8000 | SAST + supply-chain targets — modules 01, 03 |

> The third target is a placeholder — drop your own small Flask/FastAPI app
> with planted bugs into `labs/vuln-app/` so you control the source for SAST and
> the dependency tree for SBOM work.

## Bring it up

```bash
make lab-up      # docker compose up -d
make lab-down    # tear down
```

The compose file puts everything on a dedicated bridge network with no published
ports beyond localhost. Confirm with `docker compose -f labs/docker-compose.yml ps`.

## Other intentionally-vulnerable corpora used by later modules

- **Fuzzing (06):** build a target with a planted bug, or use the classics
  shipped with AFL++/libFuzzer tutorials.
- **RE (07):** crackmes from crackmes.one, or compile your own with symbols
  stripped.
- **Cloud/IaC (08):** point Checkov/tfsec at a misconfigured Terraform module
  you write under `modules/08-cloud-iac/project/`.
- **LLM security (10):** garak and PyRIT ship their own probe targets; you can
  also stand up a small RAG app to red-team.

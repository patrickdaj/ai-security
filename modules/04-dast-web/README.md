# Module 04 — Dynamic Web Security (DAST)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


Dynamic tools attack a *running* app. They're great at breadth (crawl, fuzz
params, fling payloads) and weak at two things AI helps with: writing precise
detection logic for a *newly disclosed* bug, and triaging a noisy scan into the
handful of real, exploitable issues.

## Tools you tour

- **OWASP ZAP** — full proxy + active/passive scanner; scriptable via its API.
- **Nuclei** — runs YAML templates of HTTP checks; the template format is the
  whole point. A huge community template library.
- **sqlmap** — deep, automated SQL-injection exploitation. Use against DVWA.

### Tour tasks (against the lab — authorized targets only)

```bash
make lab-up
nuclei -u http://127.0.0.1:3000 -json -o scratch/nuclei.json
zap-cli quick-scan --self-contained http://127.0.0.1:8081
sqlmap -u "http://127.0.0.1:8081/vulnerabilities/sqli/?id=1" --batch
```

Read a Nuclei template. It's a declarative request + matcher. That structure is
exactly what an LLM can *generate* from an advisory.

## AI augmentation: advisory → Nuclei template generator + scan triage

Two builds:

1. **Template generator.** Given a CVE/advisory (or a vendor bug write-up),
   produce a valid Nuclei YAML template: the request, the matchers, and severity
   metadata. Validate it by running `nuclei -validate` and against a known
   target. This turns "a bug was disclosed this morning" into "we can detect it
   org-wide by lunch."
2. **Scan triage.** Normalize ZAP/Nuclei output into `Finding`s (request +
   response into `.context`) and run the triage engine to separate
   reflected-and-exploitable from informational noise.

For the generator, use structured outputs with a `NucleiTemplate` schema, then
serialize to YAML — don't ask for raw YAML text, ask for the typed fields and
render them, so you can validate before writing.

## Exercises

1. Generate a template for a simple reflected-XSS or path-traversal advisory and
   get it to pass `nuclei -validate`.
2. Triage a Juice Shop scan; confirm the model suppresses headers-missing
   informationals while keeping the real injection findings.
3. Close the loop: generate → validate → run → feed the result back to the model
   to refine the matcher if it didn't fire.

## Done when

- You can hand the generator an advisory and get a template that actually fires
  on a vulnerable target and validates clean — and you can de-noise a raw web
  scan down to the exploitable few.

## Advanced track: manual web & API exploitation

Scanners find single issues; real assessment is *chaining* them and reasoning
about auth/session flows. Build [`project/web_chain.py`](./project/web_chain.py)
(worked answer: [`reference/web_chain.py`](./reference/web_chain.py)) to construct
multi-step exploit chains from individual findings — see
[`example-output/web-chain.md`](./example-output/web-chain.md). Lean on Burp Suite
methodology, the OWASP WSTG, and API-specific testing.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [OWASP ZAP docs](https://www.zaproxy.org/docs/)
- [Nuclei + templates](https://github.com/projectdiscovery/nuclei-templates)
- [sqlmap wiki](https://github.com/sqlmapproject/sqlmap/wiki)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

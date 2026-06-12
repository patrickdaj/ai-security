# Module 03 — Supply Chain & SBOM

Dependency scanners enumerate your packages and match them against vulnerability
databases. They are precise about *what version you have* and useless about
*whether the vulnerable code path is reachable in your app*. That reachability
gap is the entire game, and it's where AI judgment plus a little code context
pays off enormously.

## Tools you tour

- **Syft** — generates an SBOM (software bill of materials) from images/dirs.
- **Grype** — matches an SBOM against vuln data; pairs with Syft.
- **Trivy** — all-in-one: SBOM, vulns, IaC, secrets — great breadth.
- **OSV-Scanner** — Google's scanner over the OSV database; excellent data.

### Tour tasks

```bash
syft dir:labs/vuln-app -o json > scratch/sbom.json
grype sbom:scratch/sbom.json -o json > scratch/grype.json
osv-scanner --lockfile labs/vuln-app/requirements.txt --format json > scratch/osv.json
```

Notice the volume. A medium app yields hundreds of CVEs, most in transitive deps
you never call. Triaging by hand is hopeless; that's the point.

## AI augmentation: reachability + risk-narrative generator

Build a tool that, for each CVE, gathers (a) the advisory text, (b) the affected
function/symbol if the advisory names one, and (c) whether your code imports or
calls into that package's vulnerable surface. Feed all of it to the model and
ask for a reachability verdict and a one-paragraph risk narrative a human can
act on.

Map each Grype/OSV match to a `Finding` with the advisory in `.context`, then
extend the triage to answer "is the vulnerable code path reachable from our
entry points?" The model won't be certain — that's fine; surface confidence and
let it say `needs_review`.

## Exercises

1. Normalize Grype + OSV output into `Finding`s and dedup across scanners.
2. Add import-graph evidence: grep your codebase for imports of the affected
   package and include call sites in `.context`. Measure how much it sharpens
   the reachability call.
3. Generate an executive risk narrative for the top 10 by adjusted severity —
   the thing you'd actually paste into a ticket or a report.

## Done when

- You can take a 300-CVE Grype dump and produce a ranked shortlist of *reachable*
  issues with human-readable risk narratives, plus an honest "needs review"
  bucket for the ones the evidence can't decide.

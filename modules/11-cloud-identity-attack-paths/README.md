# Module 11 — Cloud Identity & Attack Paths (CIEM)

Phase: **Infrastructure & Runtime.** Cloud breaches are usually identity
breaches: an over-permissioned role, a forgotten access key, a chain of
`iam:PassRole` + `sts:AssumeRole` that walks a low-priv principal to admin.
Tools can *enumerate* permissions perfectly; what's hard — for humans — is
reasoning over the resulting graph to find the *paths*. That graph reasoning is
the single best AI-augmentation target in the whole curriculum.

## Tools you tour

- **Cartography** — ingests AWS/GCP/Azure/K8s into a Neo4j graph of assets and
  relationships. The substrate.
- **PMapper** — builds an IAM graph and computes privilege-escalation paths.
- **Steampipe** — query your cloud as if it were SQL; great for enrichment.
- **ScoutSuite** — multi-cloud posture auditor; broad misconfig coverage.

### Tour tasks (read-only creds; your own account only)

```bash
# Cartography → Neo4j, then explore relationships
cartography --neo4j-uri bolt://localhost:7687 ...

# PMapper: build the IAM graph and ask for escalation paths
pmapper graph create
pmapper query 'preset privesc *'

# Steampipe enrichment
steampipe query "select name, attached_policy_arns from aws_iam_role"
```

Look at a PMapper privesc result. It's a path: principal → permission → next
principal. Now imagine a graph with thousands of edges — finding the *important*
paths and explaining them is where the model earns its keep.

## AI augmentation: attack-path finder + least-privilege synthesizer

Build a tool that pulls candidate paths/edges (from PMapper or a Cartography
Cypher query), feeds the relevant subgraph to the model, and returns typed
[`AttackPath`](../../aug/models.py) results: entrypoint → target, the steps, a
severity and confidence, a plain-language narrative, and **the minimal policy
change that breaks the path**.

Then a second build: given a principal's *actual* used actions (from CloudTrail
via Steampipe), generate a least-privilege policy and a `Remediation` with a
breaking-change risk — the gate for whether to auto-apply.

> The model reasons over the *path data the tools computed*; it does not invent
> edges. Feed it the subgraph, ask it to prioritize and explain — not to
> hallucinate reachability.

## Exercises

1. Normalize PMapper privesc output into `AttackPath`s and rank by severity ×
   confidence; produce the top-5 narrative report.
2. Use a Cartography Cypher query to pull a blast-radius subgraph for one
   sensitive bucket and have the model explain who can reach it and how.
3. Synthesize a least-privilege policy from CloudTrail-observed actions; diff it
   against the live policy and flag the breaking changes.

## Done when

- You can turn a cloud account into a ranked, explained list of real privilege-
  escalation paths with the exact least-privilege fix for each — and you trust
  it because every step traces to an edge the tools actually found.

# Module 15 — Zero Trust Network Access (ZTNA)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


Phase: **Infrastructure & Runtime.** The perimeter is gone; "on the network" is
not authorization. Zero Trust means every request is authenticated, authorized,
and encrypted per-identity, with least-privilege microsegmentation. The
open-source ZTNA stack gives you the enforcement points; the hard, error-prone
part is *writing the policies* — least-privilege authz and microsegmentation
rules tight enough to be safe but not so tight they break the app. That policy
synthesis is where AI shines, especially when fed *observed* traffic.

## Tools you tour

- **Pomerium** — identity-aware reverse proxy; per-request access policy.
- **Ory Oathkeeper** (+ Kratos/Hydra) — identity & access proxy / authz rules.
- **OpenZiti** — programmable zero-trust overlay network (app-embedded).
- **Teleport** — identity-aware access plane for SSH/k8s/databases, with audit.
- **SPIFFE / SPIRE** — cryptographic *workload* identity (the mTLS foundation).
- **OPA** — the policy engine many of the above delegate authz to.
- **Istio / Linkerd** — service-mesh mTLS + `AuthorizationPolicy` for
  microsegmentation.

### Tour tasks

```bash
# SPIRE: issue a workload identity (SVID) and inspect it
spire-server entry create -spiffeID spiffe://example.org/web ...

# Istio: an AuthorizationPolicy allowing only one service to call another
kubectl apply -f authz-policy.yaml

# OPA: evaluate an authz decision
opa eval -d policy.rego -i input.json "data.authz.allow"
```

Map the concepts to NIST SP 800-207 (the zero-trust reference): policy decision
point, policy enforcement point, continuous verification. Then notice: the
policies are just structured allow/deny rules — generable from intent, and even
better, *inferable from the traffic you already see*.

## AI augmentation: least-privilege policy & microsegmentation synthesizer

Two builds:

1. **Policy from intent.** Given a natural-language access rule ("only the
   checkout service may call payments, only over mTLS, only POST /charge"),
   generate a [`PolicyDraft`](../../aug/models.py) — Istio `AuthorizationPolicy`,
   Oathkeeper rule, Pomerium policy, or Rego — render it, and validate
   (`opa eval`, `istioctl analyze`) against allow/deny test cases.
2. **Microsegmentation from observed traffic.** This is the high-value one and it
   ties back to **module 05**: feed the model the *observed* service-to-service
   flows (Zeek `conn.log`, mesh telemetry, VPC flow logs) and have it synthesize
   the minimal allow-list `AuthorizationPolicy` set — default-deny plus exactly
   the flows that legitimately occur — and flag flows that look like they
   shouldn't exist.

> Gate: a microsegmentation policy generated from observed traffic can lock out
> legitimate-but-rare flows. Ship it in *audit/dry-run* mode first, have the
> model explain each rule, and require human sign-off before enforcement.

Build #2 in [`project/microseg.py`](./project/microseg.py) (a stub); the worked
answer is [`reference/microseg.py`](./reference/microseg.py). It deterministically
aggregates observed flows into per-destination allow candidates, then has the model flag
anomalies (a workload hitting the cloud metadata endpoint; analytics touching
the prod DB) and emit dry-run Istio `AuthorizationPolicy` YAML for the
legitimate set. Try it:

```bash
python modules/15-zero-trust-ztna/project/microseg.py \
    modules/15-zero-trust-ztna/project/sample_flows.json --out scratch/microseg
```

## Exercises

1. Generate an Istio `AuthorizationPolicy` from intent; prove it allows the
   intended call and denies others with `istioctl`/`opa eval`.
2. Take a capture of legitimate service traffic (from module 05's Zeek output),
   synthesize a default-deny microsegmentation policy set, and verify it doesn't
   block the observed flows.
3. Issue SPIFFE workload identities and write an authz policy keyed on SPIFFE ID
   rather than IP — the essence of "identity, not network location."
4. Assess an architecture against NIST 800-207 and have the model produce a
   zero-trust maturity gap report.

## Done when

- You can generate validated least-privilege/microsegmentation policies from
  both natural-language intent and observed traffic, shipped safely in dry-run
  with human-gated enforcement — and you can articulate why identity-based authz
  replaces the perimeter.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [SPIFFE / SPIRE](https://spiffe.io/docs/)
- [Pomerium docs](https://www.pomerium.com/docs)
- [OpenZiti docs](https://openziti.io/docs/)
- [Istio AuthorizationPolicy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)
- [Open Policy Agent](https://www.openpolicyagent.org/docs/)

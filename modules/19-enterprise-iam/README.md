# Module 19 — Enterprise Identity & Access Governance

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Architecture, Identity, Crypto, Network.** Module 11 covered cloud
*workload* identity and attack paths; this is *enterprise human* identity — the
IdP, SSO protocols, joiner/mover/leaver lifecycle, privileged access, and the
access reviews auditors demand. The toil is reviewing thousands of entitlements
for over-grants and toxic combinations — exactly what AI scales.

## Tools you tour

- **Okta / Entra ID / Keycloak** — the identity providers and SSO.
- **SAML / OIDC / SCIM** — federation, tokens, and automated provisioning.
- **Teleport** — privileged access to infra (revisit from module 15).
- **IGA concepts** — access certification, segregation of duties (SoD), JML.

### Tour tasks

```bash
# Stand up Keycloak (docker), wire an app via OIDC, and inspect the tokens.
# Export a group/role-to-user mapping to feed the access review.
```

## AI augmentation: access-review + toxic-combination analyzer

Build a tool that ingests an entitlement export (who has which roles/groups/
permissions) and returns an **access review**: over-grants vs. job function,
**toxic combinations** (segregation-of-duties violations — e.g. the same person
can both create and approve payments), stale/dormant access, and a
recommendation each. See [`project/`](./project) / [`reference/`](./reference).
The model reasons over the grants you exported; it doesn't invent access.

## Exercises

1. Run an access review over an entitlement export; surface the top over-grants
   and at least one SoD violation.
2. Review an OIDC/SAML app config for common mistakes (overbroad scopes, missing
   audience checks, long-lived tokens).
3. Draft a joiner/mover/leaver policy and the SCIM provisioning rules for a role.

## Done when

- You can take an entitlement export and produce a defensible access review —
  over-grants, toxic combinations, stale access — plus sound SSO config and a
  JML lifecycle.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Okta developer docs](https://developer.okta.com/docs/) · [Keycloak docs](https://www.keycloak.org/documentation)
- [OAuth 2.0 / OIDC](https://oauth.net/2/) · [OpenID Connect](https://openid.net/developers/how-connect-works/)
- [SCIM](https://scim.cloud/) · [SAML (OASIS)](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html)
- [NIST SP 800-63 (Digital Identity Guidelines)](https://pages.nist.gov/800-63-3/)
- [Segregation of Duties (ISACA)](https://www.isaca.org/)

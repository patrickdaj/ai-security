<!-- Example output — illustrative deliverable of module 19. -->

# Access Review — Q2, Finance + Platform

420 entitlements reviewed → 7 actionable findings.

| Sev | Issue | Principal | Detail | Recommendation |
|---|---|---|---|---|
| high | toxic_combination | j.doe | holds both `ap-create` and `ap-approve` — can create *and* approve payments | split; require a second approver |
| high | over_grant | contractor-07 | in `prod-deploy` group; role is "QA analyst" | remove; QA needs read-only |
| high | stale | m.smith | `domain-admin`, last login 142 days ago | revoke; convert to JIT/PAM |
| medium | misconfig | app `billing-ui` | OIDC client allows `offline_access` + 90-day refresh tokens | scope down; shorten token TTL |
| medium | over_grant | finance-all (group) | 38 members have `gl-export`; 9 actually use it | recertify; trim to active users |

## Toxic combinations (SoD)
1 confirmed (create+approve payments). One near-miss flagged for review
(vendor-create + payment-create held by one team).

**Outcome:** 420 entitlements → a defensible access review with over-grants, an
SoD violation, stale admin access, and an OIDC misconfig — the artifact auditors
ask for, generated from the export and confirmed by you.

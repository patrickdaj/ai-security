<!-- Example output — advanced-track deliverable of module 04 (authorized target). -->

# Exploit Chain — Juice Shop (authorized)

**[critical] Account takeover via IDOR → SSRF → internal admin API**

1. `GET /api/users/42/basket` — IDOR: any user id returns its basket (broken
   object-level auth). Enumerate to harvest a target's `basketId`.
2. `POST /api/orders` with a crafted `deliveryUrl` — SSRF: server fetches the
   URL. Point it at `http://169.254.169.254/…` and at the internal order service.
3. SSRF reaches `http://orders.internal/admin/refund` (no external auth) →
   issue refunds / read other users' orders.

**Impact:** chaining three "medium" findings yields full account/data compromise
and an internal-service pivot — none of which a scanner flags on its own because
each requires reasoning about the auth flow and what the next request unlocks.

**Fixes:** enforce object-level authorization on `/api/users/*`; allowlist
`deliveryUrl` schemes/hosts; require auth on internal services (tie to ZTNA 15).

**Outcome:** individual scanner findings → one defensible, high-impact exploit
chain with the order of operations and the fix at each link.

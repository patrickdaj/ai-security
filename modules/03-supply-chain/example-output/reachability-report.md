<!-- Example output — illustrative deliverable of module 03. Hand-authored
     reference for what an SBOM reachability triage produces. -->

# Supply-Chain Reachability Report — `vuln-app`

Source: `syft` SBOM → `grype` (312 CVEs across 184 packages) → reachability
triage with `aug`. The tool found 312; **this report surfaces the 4 reachable
ones** and parks the rest.

## Reachable — act now

### CVE-2021-44228 — Log4Shell — `log4j-core@2.14.1`
- **Adjusted severity:** critical (conf 0.97)
- **Reachability:** the app logs user-controlled `User-Agent` via the affected
  logger (`AuthFilter.java:51`). JNDI lookup path is reachable pre-auth.
- **Narrative:** an attacker sets a crafted `User-Agent`; it reaches a
  vulnerable `log4j` call with default lookups enabled → RCE. Highest priority.
- **Fix:** upgrade to `2.17.1`; as a stopgap set `log4j2.formatMsgNoLookups=true`.

### CVE-2022-22965 — Spring4Shell — `spring-beans@5.3.13`
- **Adjusted severity:** high (conf 0.78)
- **Reachability:** app uses `@RequestMapping` with data binding on a JDK ≥ 9
  Tomcat deploy — the preconditions hold. **needs_review:** confirm no WAF rule
  already blocks the `class.module.classLoader` payload.

## Not reachable — deprioritized (sample of 308)

| CVE | Package | Verdict | Why |
|-----|---------|---------|-----|
| CVE-2020-8908 | guava@30.0 | not_reachable (0.85) | Vulnerable `createTempDir` never called. |
| CVE-2023-2976 | guava@30.0 | not_reachable (0.80) | Same; temp-file API unused in our code. |
| CVE-2021-37136 | netty@4.1.65 | needs_review (0.55) | Decompression path may be reachable via the upload service — confirm. |

**Outcome:** 312 CVEs → a 2-item act-now list with exploit narratives + a small
needs-review bucket, instead of a 312-row spreadsheet nobody triages.

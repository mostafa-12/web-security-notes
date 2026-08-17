# Reports Summary Table

## Table

| Link                                                                                                                                                             | Idea                                                                                                                                                          | Tip                                                                                                                                                                                                                                                 | Vuln Param                                                                                           | Vuln Method                                                                                                                                                 | Impact                                                                                                                                                        | New Web Tech                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Training Platform](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e)                 | One principle, three bypasses — components interpret the same data differently ([[03-Web-Vulnerabilities/temp.md]])                                           | Context-aware recon beats wordlists; JS files = admin blueprint                                                                                                                                                                                     | `/ReportServer`, `users.aspx`, `Users.aspx/manageUserProfile`                                        | hostname swap, trailing slash, double path, response manipulation (read-only flag `1→0`)                                                                    | Unauthenticated write access on 50k+ profiles + SSN leak                                                                                                      | [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary & Platform Misconfig]]            |
| [Cache misconfig](https://rikeshbaniya.medium.com/authorization-bypass-due-to-cache-misconfiguration-fde8b2332d2d)                                               | Authorized response cached under a public key → served to anyone inside the TTL window                                                                        | Tool contradiction (Autorize says *bypassed*, Repeater says *403*) = a signal, not a glitch; **timing is the variable**                                                                                                                             | `GetOrders` GraphQL op, `shop_id` (public ID)                                                        | Cache key misconfiguration (auth NOT in cache key) + race against the 3–4s caching window                                                                   | Full order + customer data of any shop (Critical)                                                                                                             | [[02-Web Architecture/Web Caching.md\|Web Caching — Cache Key, Micro-Caching, 3 classes]]           |
| [Vestaboard](https://rhinosecuritylabs.com/research/vestaboard-vulnerabilities/)                                                                                 | Security through obscurity: knowing the identifier (Board ID / user ID / role) is treated as proof of access — never correlated back to the authenticated JWT | Unguessable IDs ≠ safe: they stop *enumeration*, not *authorization* (the app itself hands you the IDs); UI-limited options ≠ server-enforced — tamper the `role` value; re-auth on email/password change capped the damage                         | `/simulator/[board-id]`, `/graphql` user `id`, `role` param                                          | IDOR ×3: Board ID in URL → unauthenticated read (history / logs / Google index); GraphQL `id` swap → rename any user; manual `role` tampering → Admin→Owner | Unauthenticated read of any board's content + rename any user in any tenant + Admin→Owner full tenant takeover (delete board, billing, transfer)              | [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary & Platform Misconfig]]            |
| [Plan Restriction Bypass](https://medium.com/h7w/how-i-earned-469-bounty-bypassing-plan-restriction-58f6d3120b6e)                                                | Paywall enforced in the UI only — the button is hidden, so the backend never checks the plan                                                                  | Hiding a feature ≠ restricting it: find the endpoint the paid UI calls and replay it on a free account (deep-link the settings page + hit the REST API directly; the path convention `settings/projects/{p}/plugins/{tool}` + JS bundles reveal it) | `settings/projects/<project>/plugins/<tool>/`, `PUT /api/0/projects/<org>/<project>/plugins/splunk/` | Direct navigation + crafted API request skipping the UI check (missing server-side plan/subscription check)                                                 | Free-tier users get data-forwarding (paid feature) — unauthorized data exposure (vertical priv-esc by plan tier). $469. Target: [[10-Targets/Sentry\|Sentry]] | [[11-Infrastructure/Splunk]] + Client-Side vs Server-Side checks                                    |
| [Unauthorized Role Management](https://medium.com/@bassemwanies2002/broken-access-control-to-gain-unauthorized-role-management-in-a-public-program-6925f83d0dc4) | Over-privileged JWT: UI shows "Roles & permissions disabled" but the token carries elevated scopes (`dp.entitlements.plans.read/write`) the backend trusts | The check exists server-side (JWT claims) — the bug is in *token issuance*, not a missing check; decode your own JWT and hunt for scopes a low-privilege role shouldn't hold | `/development/entitlements/roles` | Manual POST to the role endpoint — the disabled UI is cosmetic; backend authorizes from the over-granted JWT scopes | Low-privilege Backoffice Editor can create/edit/delete roles → vertical privilege escalation. Triaged as duplicate | JWT claims as the authorization boundary + scope granularity (plans vs roles sharing one namespace) |
| [First Bounty — Broken Access Control](https://medium.com/@defidev59/first-bug-bounty-reward-broken-access-control-e63ba29789f7) | GraphQL exposes a schema that acts as a built-in map of the whole attack surface — the map IS the recon, no guessing | Introspection duplicate ≠ dead end — the schema lists internal-looking fields (`ExportFileType` values like `ebl`, `khl`, `autotest`) to test one-by-one; a field-level guard missing = open even when the endpoint-level auth exists | `exportFile(type: ebl)`, `favoriteEvents(id)` | GraphQL introspection → enum value enumeration → unauthenticated query calls (`exportFile`) + ID enumeration in Intruder (`favoriteEvents`) | Unauthenticated download of an internal XML export (event details + Base64 session tokens) + viewing other users' favorite events. $940 | [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md\|Field-level authorization in GraphQL]] + session-cookie auth at endpoint ≠ per-field guard |
| [Restoring Deleted Projects](https://medium.com/@abdulrahmanreda660/restoring-permanently-deleted-projects-via-idor-7c8d8c2e3e94)                              | "Deleted" is a UI filter, not a permission revoke — a permanently deleted project was still loaded and restorable by direct ID | Error message contradicts your own action = fastest finder ("TEST already used" on a name you deleted → record still alive); state-scoped features (Restore) run on the wrong state (deleted ≠ archived); sequential IDs → enumerate deleted-neighbors | `/projects/{project-id}` (deleted), **Restore** button | Duplicate vs create inconsistency → cross-account (Manager/Owner) delete-test → direct navigation + ID swap to a deleted project → Restore without any state check | Any user restoring/enumerating permanently deleted projects in the org (soft-delete + missing state validation). Reported duplicate | [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md\|IDOR]] + Context-Dependent Access Control (object state as the boundary) + [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary]] |
| [API Misconfig → PII of 100k users](https://medium.com/@sagar_kirola-G35638/how-a-simple-api-misconfiguration-leaked-pii-of-100-000-users-326a1a29bf44)              | Participants API checks *authentication* but never *authorization* — any participant can dump a whole board; non-expiring invite codes (leaked in a stray JS file + Wayback snapshots) let anyone in | **Auth ≠ Authz** — test if the endpoint checks *this object*, not just *login*; **rotation is only surface-level** — old snapshots still hold rotated-out codes, and invites that never expire keep them valid forever | `GET /manager/api/brainstorms/{board-uuid}/participants`, invite code (`HTEN234S`) | Unauthorized participants dump (missing membership check) + hardcoded invite codes in `go.target.com/55932.js` + Wayback CDX to recover rotated codes → join board → dump 20k–100k+ records per call | PII (emails, names, UUIDs) of 100,000+ users; fixed <24h, 4-digit bounty | [[04-Recon/Wayback Machine (CDX API).md\|Wayback CDX API]] + non-expiring invite tokens (impact multiplier) |

---

## Q&A (my questions to understand the report)

> Every question is linked to the report it came from.

### From [[Training Platform - Login Bypass to Full Admin]]

*(no questions asked so far in this session — add them here as you study it)*

### From [[Authorization Bypass due to Cache Misconfiguration]]

#### Q1 — Why does the server cache for only 3/4 seconds?
**Micro-caching / short-TTL caching** — a deliberate perf pattern (Nginx/Varnish style) to absorb request spikes and cut DB load: the first `GetOrders` hits the DB, everyone else in the same 3–4s gets the cached copy. Short TTL = balance between freshness and load. **Not a mistake.** The mistake: caching a *user-specific* response **without putting the auth context in the cache key**. Rule: if the response varies by user, either don't cache it or include `Authorization` in the cache key.
→ Full tech: [[02-Web Architecture/Web Caching.md#4) Micro-Caching / Short-TTL]]

#### Q2 — Why didn't the server block the exploit like a DDoS?
- Requests look legit: valid user token + valid GraphQL query.
- Attacker mostly gets `403` → tiny responses → ~zero resource drain → no DDoS signal (DDoS detection is resource-based).
- It's low-frequency polling (≈1 req/s) to catch a 3–4s window — far under any sane rate-limit threshold, and easily distributed across accounts/IPs.
- **Rate limiting is a mitigation, not a root cause fix.** The only real fix: cache key must include auth.
→ Related: [[02-Web Architecture/Web Caching.md#9) Takeaway]]

#### Q3 — What was the key for cached response 

```
CACHE KEY =
    POST /graphql
    +
    GetOrders
    +
    shop_id=123
```
 defects here because there is no any auth techniques for checking is this cache allowed for the client or not 

### From [[API Misconfiguration - PII Leak (100k users)]]

#### Q1 — Why `collapse=urlkey` when he wants MORE invite codes?

Two different steps, two different goals:
1. **Extracting rotated codes from ONE file** → browse its snapshots directly (`web.archive.org/web/*/go.target.com/55932.js`) — **no collapse**, every historical version is a new codeset.
2. **Discovering NEW URLs across the domain** → the CDX query (`collapse=urlkey`) returns only **distinct URLs** (deduped across time). The same URL is captured 50+ times over the years — without collapse you'd get 50k rows of noise. The CDX returns URLs (`fl=original`) only; the *content* (and codes) is pulled later from each version individually.

> `collapse` removes duplicate **URLs**, not distinct **paths** — the output is still every unique endpoint the app ever had. → [[04-Recon/Wayback Machine (CDX API).md#collapse=urlkey — لما نستخدمه وإمتى]]

---

## New Techniques & Web Facts

> Full details live in the Web Architecture folder, linked from each report's row above.

1. **Micro-caching / short-TTL caching** — cache for a few seconds to absorb bursts; common on dashboard/GraphQL endpoints. → [[02-Web Architecture/Web Caching.md#4) Micro-Caching / Short-TTL]]
2. **Cache key = security boundary** — if the response varies by user and the key doesn't include auth, the cache serves one user's data to everyone. → [[02-Web Architecture/Web Caching.md#3) Cache Key — الحدود الأمنية للكاش]]
3. **Autorize as a cache oracle** — its instant replay (right after the admin call) lands inside the cache window. Contradiction between two tools = chase it. → [[02-Web Architecture/Web Caching.md#7) How to Test]]
4. **Timing-based auth bypass** — same request, admin vs user, only difference = when you send it. The bug is the window, not the code. → [[02-Web Architecture/Web Caching.md#7) How to Test]]
5. **Public ID ≠ safe ID** — `shop_id` was public and enumerable; it becomes dangerous only when combined with broken auth/caching.
6. **Cache classification** — neither classic *Web Cache Deception* (no payload, no `.css` trick) nor *Web Cache Poisoning* (no injected content): it's *cached authorized data served to unauthorized users* = a third class. → [[02-Web Architecture/Web Caching.md#5) ثلاث فئات من ثغرات الكاش]]

### From [[API Misconfiguration - PII Leak (100k users)]]

7. **Authentication ≠ Authorization (as an explicit test step)** — an endpoint can require login yet still skip the per-object membership check. Swap the `{board-uuid}`/`{id}` and compare. → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]
8. **Non-expiring invite tokens = impact multiplier** — a credential that never expires keeps any leak (even a rotated one) valid forever. → [[API Misconfiguration - PII Leak (100k users)#Key Takeaways]]
9. **Wayback snapshot versioning for rotated secrets** — browsing `https://web.archive.org/web/*/<file>` returns every historical version of that file → recover codes removed from the live copy.
10. **Wayback CDX API for domain-wide history** — `url=*.domain&fl=original&collapse=urlkey` = all distinct archived URLs (deduped) → old JS files, admin pages, backup files. → [[04-Recon/Wayback Machine (CDX API).md]]
11. **Rotation is only surface-level** — deleting a secret from the live site doesn't delete it from the archive. "Gone" ≠ gone.
12. **Scale = Impact** — judge severity by the reachable volume (20k → 100k records), not the single request.

---

## Related
- Full writeup: [[Training Platform - Login Bypass to Full Admin]]
- Full writeup: [[Plan Restriction Bypass - Free Tier to Paid Features]]
- Full writeup: [[Authorization Bypass due to Cache Misconfiguration]] *(todo)*
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
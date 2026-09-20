	# Reports Summary Table

## Table

Total: **25** reports.

| # | Link                                                                                                                                                                   | Idea                                                                                                                                                                                                                                                              | Tip                                                                                                                                                                                                                                                                                                                      | Vuln Param                                                                                           | Vuln Method                                                                                                                                                                                                                                                                            | Impact                                                                                                                                                        | New Web Tech                                                                                                                                                                                                                                       |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | [Training Platform](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e)                       | One principle, three bypasses — components interpret the same data differently ([[03-Web-Vulnerabilities/temp.md]])                                                                                                                                               | Context-aware recon beats wordlists; JS files = admin blueprint                                                                                                                                                                                                                                                          | `/ReportServer`, `users.aspx`, `Users.aspx/manageUserProfile`                                        | hostname swap, trailing slash, double path, response manipulation (read-only flag `1→0`)                                                                                                                                                                                               | Unauthenticated write access on 50k+ profiles + SSN leak                                                                                                      | [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary & Platform Misconfig]]                                                                                                                                                           |
| 2 | [Cache misconfig](https://rikeshbaniya.medium.com/authorization-bypass-due-to-cache-misconfiguration-fde8b2332d2d)                                                     | Authorized response cached under a public key → served to anyone inside the TTL window                                                                                                                                                                            | Tool contradiction (Autorize says *bypassed*, Repeater says *403*) = a signal, not a glitch; **timing is the variable**                                                                                                                                                                                                  | `GetOrders` GraphQL op, `shop_id` (public ID)                                                        | Cache key misconfiguration (auth NOT in cache key) + race against the 3–4s caching window                                                                                                                                                                                              | Full order + customer data of any shop (Critical)                                                                                                             | [[02-Web Architecture/Web Caching.md\|Web Caching — Cache Key, Micro-Caching, 3 classes]]                                                                                                                                                          |
| 3 | [Vestaboard](https://rhinosecuritylabs.com/research/vestaboard-vulnerabilities/)                                                                                       | Security through obscurity: knowing the identifier (Board ID / user ID / role) is treated as proof of access — never correlated back to the authenticated JWT                                                                                                     | Unguessable IDs ≠ safe: they stop *enumeration*, not *authorization* (the app itself hands you the IDs); UI-limited options ≠ server-enforced — tamper the `role` value; re-auth on email/password change capped the damage                                                                                              | `/simulator/[board-id]`, `/graphql` user `id`, `role` param                                          | IDOR ×3: Board ID in URL → unauthenticated read (history / logs / Google index); GraphQL `id` swap → rename any user; manual `role` tampering → Admin→Owner                                                                                                                            | Unauthenticated read of any board's content + rename any user in any tenant + Admin→Owner full tenant takeover (delete board, billing, transfer)              | [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary & Platform Misconfig]]                                                                                                                                                           |
| 4 | [Plan Restriction Bypass](https://medium.com/h7w/how-i-earned-469-bounty-bypassing-plan-restriction-58f6d3120b6e)                                                      | Paywall enforced in the UI only — the button is hidden, so the backend never checks the plan                                                                                                                                                                      | Hiding a feature ≠ restricting it: find the endpoint the paid UI calls and replay it on a free account (deep-link the settings page + hit the REST API directly; the path convention `settings/projects/{p}/plugins/{tool}` + JS bundles reveal it)                                                                      | `settings/projects/<project>/plugins/<tool>/`, `PUT /api/0/projects/<org>/<project>/plugins/splunk/` | Direct navigation + crafted API request skipping the UI check (missing server-side plan/subscription check)                                                                                                                                                                            | Free-tier users get data-forwarding (paid feature) — unauthorized data exposure (vertical priv-esc by plan tier). $469. Target: [[10-Targets/Sentry\|Sentry]] | [[11-Infrastructure/Splunk]] + Client-Side vs Server-Side checks                                                                                                                                                                                   |
| 5 | [Unauthorized Role Management](https://medium.com/@bassemwanies2002/broken-access-control-to-gain-unauthorized-role-management-in-a-public-program-6925f83d0dc4)       | Over-privileged JWT: UI shows "Roles & permissions disabled" but the token carries elevated scopes (`dp.entitlements.plans.read/write`) the backend trusts                                                                                                        | The check exists server-side (JWT claims) — the bug is in *token issuance*, not a missing check; decode your own JWT and hunt for scopes a low-privilege role shouldn't hold                                                                                                                                             | `/development/entitlements/roles`                                                                    | Manual POST to the role endpoint — the disabled UI is cosmetic; backend authorizes from the over-granted JWT scopes                                                                                                                                                                    | Low-privilege Backoffice Editor can create/edit/delete roles → vertical privilege escalation. Triaged as duplicate                                            | JWT claims as the authorization boundary + scope granularity (plans vs roles sharing one namespace)                                                                                                                                                |
| 6 | [First Bounty — Broken Access Control](https://medium.com/@defidev59/first-bug-bounty-reward-broken-access-control-e63ba29789f7)                                       | GraphQL exposes a schema that acts as a built-in map of the whole attack surface — the map IS the recon, no guessing                                                                                                                                              | Introspection duplicate ≠ dead end — the schema lists internal-looking fields (`ExportFileType` values like `ebl`, `khl`, `autotest`) to test one-by-one; a field-level guard missing = open even when the endpoint-level auth exists                                                                                    | `exportFile(type: ebl)`, `favoriteEvents(id)`                                                        | GraphQL introspection → enum value enumeration → unauthenticated query calls (`exportFile`) + ID enumeration in Intruder (`favoriteEvents`)                                                                                                                                            | Unauthenticated download of an internal XML export (event details + Base64 session tokens) + viewing other users' favorite events. $940                       | [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md\|Field-level authorization in GraphQL]] + session-cookie auth at endpoint ≠ per-field guard                                                         |
| 7 | [Restoring Deleted Projects](https://medium.com/@abdulrahmanreda660/restoring-permanently-deleted-projects-via-idor-7c8d8c2e3e94)                                      | "Deleted" is a UI filter, not a permission revoke — a permanently deleted project was still loaded and restorable by direct ID                                                                                                                                    | Error message contradicts your own action = fastest finder ("TEST already used" on a name you deleted → record still alive); state-scoped features (Restore) run on the wrong state (deleted ≠ archived); sequential IDs → enumerate deleted-neighbors                                                                   | `/projects/{project-id}` (deleted), **Restore** button                                               | Duplicate vs create inconsistency → cross-account (Manager/Owner) delete-test → direct navigation + ID swap to a deleted project → Restore without any state check                                                                                                                     | Any user restoring/enumerating permanently deleted projects in the org (soft-delete + missing state validation). Reported duplicate                           | [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md\|IDOR]] + Context-Dependent Access Control (object state as the boundary) + [[02-Web Architecture/Anatomy of a Web Request.md\|Trust Boundary]] |
| 8 | [API Misconfig → PII of 100k users](https://medium.com/@sagar_kirola-G35638/how-a-simple-api-misconfiguration-leaked-pii-of-100-000-users-326a1a29bf44)                | Participants API checks *authentication* but never *authorization* — any participant can dump a whole board; non-expiring invite codes (leaked in a stray JS file + Wayback snapshots) let anyone in                                                              | **Auth ≠ Authz** — test if the endpoint checks *this object*, not just *login*; **rotation is only surface-level** — old snapshots still hold rotated-out codes, and invites that never expire keep them valid forever                                                                                                   | `GET /manager/api/brainstorms/{board-uuid}/participants`, invite code (`HTEN234S`)                   | Unauthorized participants dump (missing membership check) + hardcoded invite codes in `go.target.com/55932.js` + Wayback CDX to recover rotated codes → join board → dump 20k–100k+ records per call                                                                                   | PII (emails, names, UUIDs) of 100,000+ users; fixed <24h, 4-digit bounty                                                                                      | [[04-Recon/Wayback Machine (CDX API).md\|Wayback CDX API]] + non-expiring invite tokens (impact multiplier)                                                                                                                                        |
| 9 | [Algolia Key Over-Exposure](https://medium.com/@Tyrion404/from-duplicate-to-bounty-88d6511dc6db)                                                                       | Public Algolia search key (extracted from a JS bundle) over-permissioned: retrieves internal financial fields, filters by moderation status, reaches a 2nd index (~80k), exposes identity facets — reported once, "Resolved", re-tested a month later, still live | **"Resolved" ≠ fixed** — re-run old reports; public keys are fine, the *permissions* on them are the boundary; wildcard query = field dictionary, then request internal fields *by name*                                                                                                                                 | `attributesToRetrieve`, `filters`, `facets`, `hitsPerPage`, `GET /1/indexes`, `/dist/server.js.map`  | JS-bundle key extraction (`grep apiKey`) → wildcard query (read full record) → explicit internal-field PoC → `filters:"restrictions:high"` enumeration → 2nd index `hitsPerPage:0` volume probe → gender facets → leaked 10.8MB server source map (2nd dev key + anti-bot bypass list) | Exact lifetime earnings + moderation decisions + gender identity for ~154,000 accounts, no auth; High severity $$$$                                           | [[Algolia Search Key Over-Exposure - 154k Records]] + [[02-Web Architecture/Algolia]]                                                                                                                                                              |
| 10 | [Manual BAC Testing](https://medium.com/@kroush333/manual-testing-for-privilege-escalation-and-broken-access-control-my-methodology-a3b9f41b82a2)                      | Authorization check is **presence-based** — only runs if the `user` object is in the body (delete it → check skipped → `200 OK`); server trusts the client-supplied `permissions` array                                                                           | **Weaknesses:** (1) check fails-open when the target object is missing (no fail-closed); (2) server accepts role/permission data from the client without comparing it to the token's role — **rejected deleting permissions (`permissions: []` → blocked) but accepted adding the Admin's array → became project Admin** | `user` JSON object (removed from body), `permissions` array (Admin's array copied in)                | Manual matrix testing (role × function) + one token per role → body tampering: delete `user` → `200 OK` (user removed, re-send re-adds) → inject Admin's `permissions` array                                                                                                           | Member → project Admin (vertical privilege escalation / BAC). Reported → duplicate                                                                            | [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md\|Never Trust Client-Controlled Data]] + presence-based authorization (missing = allow)                                                                                  |
| 11 | [IDOR + Public S3 Report](https://c0nqr0r.medium.com/idor-and-broken-access-control-risking-private-data-exposure-dd808412ed13)                                        | Report generation is an **async background job** — `postId` → `backgroundJobId` (ownership never checked); the PDF lands on a **public S3 bucket** via a plain unauthenticated URL                                                                                | **UUIDs are references, not permissions** — unguessable ≠ authorized; test *every* export path (email vs PDF); when you see an `s3.amazonaws.com/...` URL, check object-public *and* ListBucket; sequential IDs → mass enumeration (respect scope: prove with a few IDs)                                                 | `postId`, `backgroundJobId`, `GET /api/reports/result/{jobId}`, S3 `downloadUrl`                     | IDOR on `POST /api/reports/generate` (no `post.owner == session.user` check) → Intruder over post IDs (0→9,999,999) collecting valid job IDs → direct download from public S3                                                                                                          | All users' private post reports downloadable (mass data exposure) — High/Critical                                                                             | [[11-Infrastructure/Amazon S3.md\|Amazon S3 — public objects vs ListBucket]] + async-job pattern as an attack surface                                                                                                                              |
| 12 | [From Internal User to Admin](https://medium.com/@mobadawyx4/from-internal-user-to-admin-exploiting-broken-access-control-in-saas-platforms-c1a2e36489a4)              | UI hides role selector for Internal Users; backend accepts `companyUserRoles` on `/contacts` without verifying requester can assign those roles                                                                                                                   | Map all endpoints for a feature — same feature (invite) has two endpoints with different authz; diff the payloads, replay high-priv with low-priv token                                                                                                                                                                  | `companyUserRoles[]` (array), `identifiers[]`, `contactType`                                         | Replay Admin invitation request (`POST /api/v1/contacts`) with Internal User token + elevated roles payload; CSRF token is same-session readable                                                                                                                                       | Internal User → creates Manager/Administrator accounts → full org compromise (invite more admins, access data, change settings)                               | [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md\|Endpoint differentiation as recon]] + Multi-tenant RBAC role-granting surface                                                                       |
| 13 | [Breaking Trust, Not Cryptography](https://wadgamaraldeen.medium.com/how-i-found-a-critical-jwt-authentication-design-flaw-and-earned-a-1-450-bug-bounty-4ea6bbd90bb5) | Refresh token treated as sole source of truth — backend validates signature only, zero server-side session binding, no jti/rotation/device context                                                                                                                | **Stateless ≠ secure** — a valid JWT ≠ valid session; delete all cookies except refresh token, if auth still works → single source of truth flaw                                                                                                                                                                         | `__Host-refreshToken` cookie (JWT), `sub` claim                                                      | Token theft (XSS/logs/MITM) → replay to `/refresh` → backend extracts `sub` from valid signature → issues new access tokens; no session lookup, no revocation, no rotation                                                                                                             | Critical — Zero-click account takeover until token expiry (6 days), any token compromise = full access, no defense in depth                                   | [[JWT Refresh Token Design Flaws]] + [[Server-Side Session Binding]] + [[Refresh Token Rotation & Reuse Detection]]                                                                                                                                |
| 14 | [Auth Bypass via .php Removal](https://...)                                                                                                                            | Protected endpoint `/videos.php` requires auth; same resource accessible via `/videos` (extension removed) — access-control middleware checks URL, router normalizes to same PHP app                                                                              | **Protected endpoint ≠ protected resource** — test every URL form that reaches the same functionality; custom 404 pages leak attack surface                                                                                                                                                                              | `/videos.php`, `/videos`, `/media/`                                                                  | Extension removal (`/videos.php` → `/videos`) + directory listing on `/media/`                                                                                                                                                                                                         | Unauthenticated access to all user videos + full file enumeration via directory listing                                                                       | [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md\|Step 4 — Try Alternative Requests]] + [[04-Recon/Manual Browsing.md]]                                                                               |
| 15 | [Easy P3 BAC — Employee Profile](https://medium.com/@a0xtrojan/easy-p3-broken-access-control-7c28702cb1ee) | Employee profile read-only in UI but writable via direct API replay — Admin-only edit enforced client-side only | **Read-only UI = bypass signal** — if the GET exists, hunt the PUT/PATCH in Burp history/JS and replay with low-priv token; prove with harmless `name` field first | profile-update endpoint (path redacted), `name`/`mobile`/`timezone` | Two-account setup (Admin+User) → capture Admin update in Burp → replay with Employee session → `200 OK` | Low-priv employee edits profiles (P3). Triaged then duplicate | [[Easy P3 Broken Access Control - Employee Profile Update]] + Client-Side vs Server-Side |
| 16 | [Gmail API Attachment IDOR](https://material.security/resources/how-material-security-uncovered-a-vulnerability-in-the-gmail-api) | Attachment-fetch endpoint trusts `attachmentId` alone — issuing endpoint checks ownership, consuming endpoint doesn't; `messageId` ignored (`"foo"` works) | **Unstable ID = discovery signal** — same object returning different IDs per read (+ old IDs valid) means a backend association table; permute each reference + try garbage values | `attachmentId`, `messageId` (`users.messages.attachments.get`) | Cross-owner permutation + `messageId="foo"` garbage test with attacker OAuth token → `200 OK` + bytes | Any authenticated Google user reads any Gmail attachment (capped by ID entropy, not authz). Fixed by Google | [[Gmail API Attachment IDOR - Missing Object-Level Authorization]] + BOLA/IDOR |
| 17 | [Django Debug → PII (500+)](https://medium.com/@fa1c0n/from-django-debug-mode-to-pii-data-leak-of-more-than-500-employees-due-broken-access-control-and-a3eb602a4207) | Internal subdomain on 443 (open signup) + 8443 (DEBUG + Swagger) sharing one backend → own JWT in Swagger Authorize → bare-`id` IDOR | **Ports are not boundaries** — same subdomain new port = new app; DEBUG page → hunt docs; docs + weakest account = fastest IDOR loop | bare `id` (employee endpoints), JWT (cross-port reuse), `/swagger`+`/redoc` | subfinder/amass/assetfinder→alterx→httpx→naabu→nuclei; random-path DEBUG probe; own-JWT-in-Swagger; `id` swap | PII (names, work emails, phones) of 500+ employees | [[Django Debug Mode to PII Leak (500+ Employees)]] + DEBUG/Swagger deep-dives |
| 18 | [Facebook Analytics Private Chart](https://bugreader.com/jubabaghdad@disclose-private-dashboard-charts-name-and-data-in-facebook-analytics-184) | Private visibility enforced on Dashboard (parent) but not on Chart (child) — Sub-option forgotten | **Sub-option audit:** Private/Owner-only on parent → hunt the direct child endpoint; Delete/Update mutations echo the object → read the returned `node` | `chartID`, `doc_id=1297068037067230` (`AnalyticsChartDeleteMutation`) | Cross-role replay: Analyst token + victim `chartID` on `POST graph.facebook.com/graphql` → `200 OK` + title/query spec | Analyst reads Admin owner-only chart name + data (LOW, VALID, bounty Apr 2020) | [[Facebook Analytics Private Chart Disclosure via IDOR]] + BOLA/IDOR |
| 19 | [Facebook Event Co-Host IDOR](https://bugreader.com/binit@adding-anyone-including-non-friend-and-blocked-people-as-co-host-in-personal-event-181) | Friend-only Co-hosts picker enforced in UI only — submit endpoint trusts `co_hosts[0]` alone, no friendship/block check | **Friendly-ID swap:** pick valid friend to satisfy UI, swap to stranger/blocked ID in Burp; test block matrix both directions; no-reject = severity upgrade | `co_hosts[0]` (`POST /ajax/create/event/submit/`) | Intercept create event (friend 1008) → swap to victim 31337 → forward → pending co-host + forced notification | Anyone (non-friend / blocked either way) forced as public co-host, no reject — harassment primitive. $750 MEDIUM VALID | [[Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]] + BOLA/IDOR |
| 20 | [Facebook Video Poll Deletion](https://bugreader.com/testgrounds@deleting-anyones-video-poll-175) | Video save checks parent `v` + `av` but never binds child `deleted_poll_ids[0]` to that video — valid parent + foreign child = delete | **Delete-array swap:** build own video+poll to reach save path, intercept delete-save, swap only child ID; new sub-features first | `deleted_poll_ids[0]` (`POST /video/edit/dialog/save/?v=&av=`) | Own video+poll → intercept delete-save → swap to victim `POLL ID` → forward → victim poll deleted | Anyone's video poll deletable (integrity break, no read). MEDIUM VALID, fixed Nov 2018 | [[Facebook Video Poll Deletion via IDOR]] + BOLA/IDOR |
| 21 | [Unauthenticated Payment (CWE-306)](https://medium.com/@mgsa112233/bypassing-access-controls-how-i-found-an-unauthenticated-payment-processing-endpoint-cvss-8-5-02d972bcd57c) | Critical payment function with no server-side auth — `Origin`/CORS trusted as the gate; public `/v3/api-docs` maps the flow, `/session` mints live context, `/process-payment` reaches live Cybersource | **Follow the flow, prove side effects:** docs → mint step → redeem step; forged `Origin` via curl; transaction-ID = liveness proof, not `200 OK`; payment-session ≠ login-session | `/v3/api-docs`, `/microforms/session` (`amount/currency/product`), `/microforms/process-payment` (`transientToken/vgNumber`) | Public docs → unauth `POST /session` (live `captureContext` JWT) → unauth `POST /process-payment` (`not-a-real-token`) → real transaction IDs | Unauth reach to live payment processor + merchant JWT + internal product map (CVSS 8.5 High, CWE-306+CWE-200). Triaged/Open | [[Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]] + CWE-306 vs IDOR |
| 22 | [Travel Booking IDOR (bookingId)](https://medium.com/@romene.mohtadi.it/from-idor-to-fraud-breaking-access-control-in-a-travel-booking-platform-ef63f6b0bb2b) | Two booking-read endpoints trust sequential `bookingId` with no ownership check — `±1` decrement leaks another user's PII + itinerary; fraud chain claimed but only read proved | **±1 decrement first:** `180845→180844` before Intruder; twin-endpoint check (`getbooking` + `getbookingFlight`); **proved-vs-possible split** (PII proved, ATO/refund needs write PoC) | `bookingId` (`GET /fr/account/getbooking`, `GET /fr/account/getbookingFlight`) | Auth session → Repeater swap `180845→180844` → `200 OK` + victim PII; sequential IDs → Intruder scale (prove with 2 own accounts) | Mass PII + itinerary leak (phishing/support-impersonation ready). Fraud/ATO = possible, not proved — title overkill | [[From IDOR to Fraud - Travel Booking Platform bookingId]] + BOLA/IDOR |
| 23 | [Live Share Accept Bypass ($250)](https://medium.com/@tonmoydatta495/how-i-got-regular-users-to-bypass-admin-approval-and-accept-live-shares-broken-access-control-c4e086da86ec) | Inbound live-share accept locked to Org/Account Admin in docs/UI but enforced nowhere on accept path — regular user clicks email `Accept Invitation` → share goes org-wide | **Who can ACCEPT?** — two-party workflows: harden both sides; email link is a first-class endpoint entry, not UI leftovers; prove role + result in one PoC | accept live-share action (email `Accept Invitation`, share `Pending→Accepted`) | Two-org setup (A sender, B receiver regular user) → accept via email link with low-priv session → `SUCCESS` + org-wide visibility, no `403` | Regular user pulls external live test feed into whole org with zero admin approval (governance/compliance break). P4 $250 | [[Live Share Accept Bypass - Regular User Bypasses Admin Approval]] + state-transition BAC |
| 24 | [Missing Link ATO](https://medium.com/@belalshohaip222/the-missing-link-how-a-broken-access-control-led-to-a-full-account-takeover-ato-607436c5b636) | Password change = `Authenticate` → `Set` on `POST /apiv1` with no linking token/flag — UI sequence trusted as proof; `Set` alone accepts injected `password` | **What is the link?** — two sequential calls = unlinked until proven; drop step 1, replay step 2 alone; generic `Set` + `entity` = mass-assignment fuzz surface | `password` in `Set` `entity` (`POST /apiv1`, `typeName: User`) | Skip `Authenticate`, send `Set` with `"password":"Hacking@123"` on attacker session → `200 OK` → fresh incognito login proves ATO | Session-only → permanent lockout; Fleet Admin = ops paralysis + safety + SLA loss (Critical) | [[The Missing Link - Broken Access Control to Full ATO]] + [[03-Web-Vulnerabilities/Methodology/BAC-Password-Change-and-Mass-Assignment.md]] |
| 25 | [Frontend Security Is Not Enough](https://medium.com/@albertstive1010/frontend-security-is-not-enough-a-practical-demonstration-of-broken-access-control-in-rest-apis-02d4f6fe4cbd) | Admin page flashes <2s then JS-crashes on `unauthorized` — frontend guard only; backend API already returned admin JSON | **Flash = clue, not finding:** keep JS on so fetch fires, read `Network → Fetch/XHR` before the crash; decisive PoC is `Copy as cURL` + low-priv replay (`200` vs `403`); `301/302` on ffuf always gets a manual visit | `/admin` path + `/api/admin/*` XHR endpoints (paths redacted) | FFUF hidden-path enum → fresh tab + DevTools Fetch/XHR read → curl/Repeater replay with low-priv session | Regular user reads admin API responses (vertical BAC / missing function-level authz) | [[Frontend Security Is Not Enough - Broken Access Control in REST APIs]] + multi-step-function BAC |

---

## Q&A (my questions to understand the report)

> Every question is linked to the report it came from.

### From [[Training Platform - Login Bypass to Full Admin]]

*(no questions asked so far in this session — add them here as you study it)*

### From [[Authentication Bypass via .php Extension Removal]]

*(add questions here as you study it)*

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

### From [[Algolia Search Key Over-Exposure - 154k Records]]

#### Q1 — Was the frontend also receiving these internal fields?
Almost certainly **yes in the raw response** — Algolia's default (`attributesToRetrieve` omitted) returns *all* attributes. The frontend just doesn't render them. **Client-side filtering ≠ security** — the fields were retrievable at the API level for everyone. → [[Algolia Search Key Over-Exposure - 154k Records#Q4 — Did the frontend also request these internal fields?]]

#### Q2 — How did he discover the exact internal field names?
Wildcard query first → full record JSON → read names (`internal_engagement_scores`, `computed_features_order_counts`, `restrictions`) → then craft the explicit PoC with those exact names. The raw JSON *is* the field dictionary.

#### Q3 — How did he know `restrictions` is filterable?
Filter syntax is standard Algolia (`"filters": "field:value"`). Whether it works is the oracle: non-filterable → `attribute is not filterable` error; it succeeded → the field was enabled under `attributesForFaceting`.

#### Q4 — How did he find the second index?
Not stated in the write-up. Realistic: JS bundle, naming-pattern guess, or the leaked source map. Reliable route not in the article: `GET /1/indexes` lists every index the key can reach.

#### Q5 — Did the researcher "study" Algolia like a developer?
No — hunter-shaped reading: the Security Guidelines sections + the parameters that control access + common misconfigs, then experimenting on a free test account. Same logic transfers to Meilisearch/Typesense/Elasticsearch/S3/Firebase/GraphQL. → [[Algolia Search Key Over-Exposure - 154k Records#Q8 — Did the researcher "study" Algolia like a developer?]]

### From [[IDOR + Public S3 Report Exposure]]

#### Q1 — Why didn't the email-report path leak the data (and the write-up calls it "secure")?
The email recipient was resolved **server-side** (bound to the session account / post owner), not taken from the request — so the attacker couldn't redirect someone else's report to their own inbox. That fixed the *delivery*, but never fixed the **ownership check**. The same missing check simply waited in the PDF path.

#### Q2 — If the `backgroundJobId` is a UUID, why "brute-force" the reports?
You don't brute-force the UUID (128-bit, unguessable). You brute-force the **sequential `postId`** in front of it — each valid `postId` hands back a valid job ID. The UUID is only as strong as the narrowest way to obtain it; the predictable ID made it obtainable.

#### Q3 — If the result endpoint (`GET /api/reports/result/{jobId}`) had an authorization check, could the data still leak?
Yes — through the **storage layer**: (1) if the S3 bucket also allows `ListBucket`, every file is enumerable with zero knowledge (UUID irrelevant); (2) if the plain `downloadUrl` leaks anywhere (logs, referrers, shared links), it stays valid with no auth. Defense in depth = the API fix alone isn't enough.

#### Q4 — Is "IDOR + Broken Access Control" really two separate bugs?
Same root cause (missing object-level authorization) at **two layers** — API (job generation) and storage (public file access). Reports often file them as two findings to reflect the two independent fixes; the genuinely distinct issue is the public bucket, not the IDOR label.

### From [[From Internal User to Admin - Broken Access Control in SaaS]]

#### Q1 — How did the attacker get the CSRF Token?
The attacker *is* the Internal User — they own the session. The CSRF token lives in their browser: Cookie (`csrf_token=...`), HTML meta tag (`<meta name="csrf-token" content="...">`), JS variable (`window.csrfToken`), or response header. CSRF tokens protect against *cross-site* forgery (evil.com → app.com), not *same-session* abuse. The session owner reads their own token and uses it in the exploit request.

#### Q2 — Is the CSRF Token per-request (rotating) or per-session?
Test it: send the same request twice in Burp Repeater with the same token.
- `200 OK` both times → **per-session / time-limited** (not rotating).
- `403 Invalid CSRF` on second try → **per-request / rotating** (requires automation: GET page → extract → POST immediately).
Most SaaS apps use per-session or short-TTL (15–30 min) tokens. → [[07-CheatSheets/Session-Management.md#CSRF Token Patterns|CSRF Token Patterns]]

#### Q3 — Why does `/api/v1/contacts` check Authentication but not Authorization?
Common confusion: **Authentication = "Who are you?"** (valid token) — **Authorization = "What can you do?"** (can you assign `manager`?). The endpoint validated the token (AuthN) but skipped the `can_assign_role(requested_role)` check (AuthZ). The parameter `companyUserRoles` came from the request body — client-controlled — and the server trusted it.

#### Q4 — What is the fundamental difference between `/companyjoinrequests` and `/contacts`?
| Endpoint | Actor | Purpose | `roles` param |
|----------|-------|---------|---------------|
| `POST /api/v1/companyjoinrequests` | Internal User | Join request (pending/low-priv) | **Absent** |
| `POST /api/v1/contacts` | Administrator | Direct invite **with role assignment** | **`companyUserRoles[]`** (e.g., `["user", "manager"]`) |

The vulnerability: the **Admin endpoint** (`/contacts`) accepts the role parameter but **doesn't verify the caller is an Admin**.

#### Q5 — How do you test for multi-tenant RBAC bypass in other SaaS platforms?
1. **Map endpoints per role** — Login as Admin, Internal User, Viewer. Record every invite/member/add-user request.
2. **Diff the payloads** — What parameters exist in Admin requests but not in User requests? (`roles`, `permissions`, `plan`, `tier`, `accessLevel`).
3. **Replay with low-priv token** — Send the Admin payload (with elevated roles) using the Internal User's token/cookies.
4. **Test the matrix** — Requester Role × Target Role: Can Viewer assign Manager? Can Manager assign Admin? Can Internal assign Manager?
5. **Check parallel endpoints** — `/invitations`, `/memberships`, `/users`, `/contacts`, `/organization/members` — same feature, different paths.

### From [[Easy P3 Broken Access Control - Employee Profile Update]]

#### Q1 — How do you test a "read-only" profile page for BAC?
The read-only page proves the `GET` (read) path exists. Find the write path: check Burp Proxy history while acting as Admin, search JS bundles for `PUT/PATCH /profile|/employee|/member`, then replay that request with the Employee session token. `200 OK` + changed value on refresh = missing server-side authz.

#### Q2 — Why start with the `name` field and not something sensitive?
`name` is low-risk, highly visible, non-destructive proof of write access. It confirms the bypass without corrupting data. Once proven, escalate mentally: same endpoint may allow `email` (takeover), `role` (priv-esc), `user_id` (IDOR).

### From [[Gmail API Attachment IDOR - Missing Object-Level Authorization]]

#### Q1 — Why did `messageId="foo"` still return data?
The endpoint resolved the attachment **by `attachmentId` alone** and never validated `messageId` (no existence check, no `attachment.message_id == request.message_id`, no ownership check). `messageId` was a decorative parameter — the server ignored it. One garbage-value request proves non-validation decisively.

#### Q2 — If `attachmentId`s are unguessable, why is this still a vulnerability?
Unguessable IDs stop *enumeration* (no brute force), not *authorization*. The IDs leaked through normal channels: orgs/apps logging them, third-party apps storing them, old IDs staying valid 1+ year after OAuth revocation. Any leaked ID = full attachment content. Entropy caps scale; it never replaces the `owner == requester` check.

### From [[Facebook Analytics Private Chart Disclosure via IDOR]]

#### Q1 — Why does direct chart fetch bypass the dashboard check?
Two independent resolvers: `dashboard(id){charts{...}}` checks `visibility + owner`, but `node(chartID)` / `AnalyticsChartDeleteMutation(chartID)` does `get_chart_by_id()` with no parent context. Logically nested in UI, technically standalone rows with global IDs.

#### Q2 — Why does a Delete mutation leak data?
GraphQL mutations echo the affected `node` back (title + query spec) before/instead of deleting. A forbidden write becomes a successful read — always inspect the returned object.

### From [[Django Debug Mode to PII Leak (500+ Employees)]]

#### Q1 — Why does a random path like `/hacker` reveal DEBUG mode?
A valid path renders normally; an *invalid* path forces an exception. With `DEBUG=False` you get a generic "Server Error (500)". With `DEBUG=True` Django renders the yellow technical page (routes, settings context, traceback + source, env) — designed for developers, served to attackers. One garbage path distinguishes the two states.

#### Q2 — Why did the 443 JWT work on 8443's API?
Both ports share one backend: same user DB, same JWT `SECRET_KEY`, no `aud`/scope separation. The token's signature verified on both surfaces because it's the same verifier. Port-only "dev vs prod" separation is one trust domain — the weaker surface (docs, debug) inherits the stronger surface's authority.

#### Q3 — Why hunt Swagger/Redoc right after finding DEBUG mode?
Frameworks commonly auto-mount docs routes under debug/dev settings and teams forget to unmount them in prod — they travel together. Docs give completeness (every endpoint, labeled params) + a built-in exploit console (Authorize + Try it out), beating wordlists for discovery.

### From [[Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]]

#### Q1 — Why didn't the friend-only picker stop the attack?
The picker is client-side UX. The submit endpoint (`POST /ajax/create/event/submit/`) accepted raw `co_hosts[0]` with no `are_friends(host, id)` check. Pick a valid friend to pass the UI, swap to victim ID in Burp — any allowlist enforced only in the browser is replayable.

#### Q2 — Why did block in either direction still allow the add?
The endpoint never queried the block graph — no `is_blocked(A,B) OR is_blocked(B,A)` check before creating the link or sending the notification. Block hid content visibility but was never an authorization input to this write.

#### Q3 — Why does "no reject + auto-public" upgrade severity?
A dismissible invite is spam. Forced + publicly listed as host with no decline path = reputational harm / harassment primitive (attach anyone to scam/political/abusive events). That's what lifted it to MEDIUM + $750.

### From [[Facebook Video Poll Deletion via IDOR]]

#### Q1 — Why did a valid `v` + `av` still delete someone else's poll?
The save endpoint validated `user can_edit(video)` from `?v=&av=` but resolved `deleted_poll_ids[0]` by ID alone — no `poll.video_id == video.id`, no `poll.owner == requester`. Parent check passed, child check missing, so any poll ID was deletable.

#### Q2 — Why build your own video + poll first instead of attacking directly?
The vulnerable code path (poll delete-save) is only reachable with a valid parent you own. Your own video + poll satisfies the UI + parent check, then Burp lets you swap only the child ID to the victim's on the way out.

### From [[Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]]

#### Q1 — Is a payment session the same as a login session?
No. Login = identity (`who is the user?`). Payment session = flow context (`prepare → context → process`). Getting a `captureContext` proves context creation, not a charge.

#### Q2 — Why isn't unauthenticated `/session` alone enough?
Some checkouts start pre-login legitimately. The finding is the redeeming step: `/process-payment` performing the state-changing action without auth.

#### Q3 — Why does forged `Origin` + curl bypass the gate?
`Origin` is client-controlled; only browsers enforce CORS. `curl`/Burp/Python send any header, so `correct Origin = allowed` never proves an authenticated user.

#### Q4 — What proved live-processor reach, and what was NOT proved?
Real Cybersource transaction IDs = liveness (not just `200 OK`). NOT proved: free purchase, victim charge, payout, PAN/CVV use — researcher used `"not-a-real-token"` and stopped.

### From [[From IDOR to Fraud - Travel Booking Platform bookingId]]

#### Q1 — Why is `180845 → 180844` enough for a valid PoC?
Decrement-by-one returning `200 OK` + a different user's PII on an authenticated endpoint proves the ownership check is missing. Two own accounts (A reads B, B reads A) make it clean without touching prod users.

#### Q2 — If both `getbooking` and `getbookingFlight` are vulnerable, is that two bugs?
Same root cause (missing `owner == requester` check) in shared booking code — file as one systemic BAC, show both endpoints as evidence. Fix once in the centralized authz layer.

#### Q3 — Is the fraud chain real or overkill?
Half-overkill. Phishing + support impersonation follow directly from leaked PNR/KBA fields. ATO + refund/modification fraud need a separate write PoC (`POST /cancel|/refund|/modify`) that was never shown — report as `possible`, not `proved`.

#### Q4 — Does PII alone justify High/Critical without proving fraud?
Yes. Mass-readable names + emails + phones + travel movement via sequential IDs = privacy breach + GDPR risk + high-fidelity phishing. No need to inflate to ATO to make it Critical.

### From [[Live Share Accept Bypass - Regular User Bypasses Admin Approval]]

#### Q1 — Why test the accept side if the invite side is already protected?
Invite and accept are two independent authorization boundaries. The sender org checks "who can share?", the receiver org must check "who can pull external data in?" The write-up proves the second check was missing — RBAC on `Send` never implies RBAC on `Accept`.

#### Q2 — Why is email-link accept a distinct attack surface from the dashboard button?
The dashboard button can be hidden for regular users (client-side), but the email link reaches the same server endpoint directly with the invite token. If the endpoint doesn't verify `role == Org Admin / Account Admin`, hiding the UI changes nothing — the email is the bypass.

#### Q3 — Why does one regular-user accept affect the whole org (blast radius)?
Accept flips share state `Pending → Accepted` at org scope, not user scope. The object becomes `visible_to_org(receiver_org)`. So the finding is not self-read — it's a low-priv write that forces external data on every member, which is the severity lever (governance + compliance).

### From [[The Missing Link - Broken Access Control to Full ATO]]

#### Q1 — What exactly linked (or didn't link) `Authenticate` → `Set`?
Nothing. No token returned by `Authenticate`, no session flag set, no `oldPassword` required inside `Set`. The UI waited for step-1 success before sending step 2, but the server never verified that ordering. Two requests to the same `POST /apiv1` with only a shared `sessionId` = no authorization link.

#### Q2 — Why is a valid session enough, with no old password or email access?
The vulnerable `Set` endpoint checked authentication (`sessionId` valid) but not authorization context (fresh credential proof for a password change). Any session holder — unlocked terminal, hijacked cookie — could write `password` directly. No need for phishing or reset-token theft.

#### Q3 — Why did `200 OK` need a fresh-login proof?
`200 OK` proves a write happened, not whose credential changed or whether it persists. Incognito login with victim email + new password proves the write landed on the victim object and is usable — that upgrades the finding from "profile write" to "ATO".

#### Q4 — What are the two valid fixes, and when to use each?
Single-request `oldPassword` check (simplest — verify hash in the same `Set` call) for normal password-change forms; single-use short-lived token (issued by `Authenticate`, consumed by `Set`) when the two-step architecture must be kept. Both enforce the check server-side per request.

### From [[Frontend Security Is Not Enough - Broken Access Control in REST APIs]]

#### Q1 — Why not just disable JS and read the full response?
Full JS disable often stops the SPA `fetch` itself — no request, no leak to read. The author's `Fetch/XHR` timing keeps JS on so the API call fires, then reads the response before the guard crashes the page. Decisive PoC stays `curl`/Repeater with the low-priv session.

#### Q2 — Why would the dev "send the full response then the check"?
They usually don't sequence it — the server returns `200 + data + JS` and the client decides (`if admin → show, else crash`). Once the JSON reaches the browser it is already on the attacker side (Burp/Network). "Send verify-JS first" is still client-side and bypassed by one direct API call; the fix is a per-request server-side role check returning `403` before data.

#### Q3 — Is this IDOR or vertical BAC?
As described it is **vertical BAC / missing function-level auth** (low role → admin function), not an object-ID swap. If a later step in the same workflow also takes a victim `id`, that step gets its own IDOR test — hence the multi-step lens: `reach → see data → select object → perform action`, authorize every step.

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

### From [[Algolia Search Key Over-Exposure - 154k Records]]

13. **Wildcard query = field dictionary** — omit `attributesToRetrieve`; the full record JSON reveals hidden/internal field names.
14. **`filters` as a permissions oracle** — `field:value` succeeding = field also enabled for faceting/filtering.
15. **`hitsPerPage: 0` volume probe** — count records (`nbHits`) without downloading any data.
16. **Facets for sensitivity proof** — aggregate counts (gender, categories) = impact proof without dumping records.
17. **`GET /1/indexes` index enumeration** — with the key, list every index it can reach (no guessing).
18. **Source-map probing** — `.map` on bundle paths or `/dist/*.map`; a *server-side* map = full source + secrets + defense-bypass map.
19. **Cross-index key testing** — one key may unlock sibling indexes (`*_v0`, `*_business_*`).
20. **Re-audit closed reports** — partial remediation (fix applied to one index only) = new high-value finding.
21. **Public key ≠ public data** — public search keys are by-design public; the *permissions* (retrievable/filterable attributes, index scope) are the boundary. Fix: `unretrievableAttributes` + per-index key scoping + no source maps in prod.
22. **DSN vs main API surface** — `-dsn.algolia.net` = read/search surface; `.algolia.net` = main/admin API. Knowing the surface clarifies what a key should do.

### From [[IDOR + Public S3 Report Exposure]]

23. **Async background-job pattern = IDOR surface** — a feature that returns a job reference (`backgroundJobId`, `taskId`) has *two* requests to authorize: the one that creates the job (swap the object ID) and the one that fetches the result (is the job ID yours?). → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]]
24. **One "secure" path ≠ all paths secure** — email and PDF export for the same data are independent surfaces; the same missing ownership check can live on the other one.
25. **Storage URLs are a separate trust domain** — a `downloadUrl` on S3 is a different boundary than the API that produced it. Test it on its own: plain vs presigned, object-public vs list-public. → [[11-Infrastructure/Amazon S3.md|Amazon S3]]
26. **UUID ≠ authorization** — unguessable ≠ authorized. Any endpoint that hands out a UUID without ownership checks destroys its secrecy. Never brute-force a UUID; brute-force whatever sequential ID sits in front of it.
27. **S3 list oracle** — `?list-type=2` or `aws s3 ls s3://<bucket>/ --no-sign-request`; anonymous list = whole dataset with zero knowledge. → [[11-Infrastructure/Amazon S3.md#2) ListBucket عام — الـ enumeration — الأسوأ]]
28. **Respect scope on enumeration** — proving impact on a few IDs + stating "full enumeration possible" beats a 10M-request sweep that gets you banned.

### From [[From Internal User to Admin - Broken Access Control in SaaS]]

29. **Endpoint differentiation as recon** — The same business feature (invite user) exposes **two endpoints** (`/companyjoinrequests` vs `/contacts`) with different privilege requirements. Finding *all* endpoints for a feature reveals the one with missing authz. → [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]]

30. **`companyUserRoles` / `roles` parameter as privilege escalation vector** — Any parameter that assigns roles/permissions to *another* user must be validated against the requester's **maximum assignable role**, not just their authentication status. Test: add `roles: ["admin"]` to any create-user/invite/membership endpoint.

31. **Multi-tenant SaaS: role-granting endpoint ≠ self-role endpoint** — The endpoint that *grants roles to others* (`/contacts`, `/invitations`, `/memberships`) is a distinct attack surface from the endpoint that *changes your own role* (`/profile`, `/account`). Test both independently.

32. **CSRF token in same-session exploit = not a barrier** — CSRF tokens are per-session secrets readable by the session owner. They prevent *cross-origin* forgery, not *authorized-user* abuse of an over-permissive endpoint. If you own the session, you own the CSRF token.

33. **Duplicate finding ≠ low severity / not reproducible** — "Closed as duplicate" means the pattern is known and recurring in the platform. Test for it anyway; a duplicate in one program may be a valid finding in another. The pattern (UI-hiding + missing server-side authz on role-granting endpoint) is generic.

### From [[Easy P3 Broken Access Control - Employee Profile Update]]

34. **"Invite-then-edit" setup as BAC scaffold** — Admin invites your own second account → you control both sides (inviter + invitee) and can diff their requests.
35. **Read-only UI as bypass signal** — displayed-but-not-editable profile implies a hidden write endpoint (`PUT/PATCH /profile|/employee`); find it in Burp history/JS and replay with low-priv token.
36. **Harmless-field-first PoC** — prove write with `name=HACKED` before touching sensitive fields (`email`, `role`, `user_id`).

### From [[Gmail API Attachment IDOR - Missing Object-Level Authorization]]

37. **Unstable ID as discovery signal** — same object minting a different ID per read (+ old IDs staying valid) = backend association table; immediately permute cross-owner + garbage sibling values.
38. **Permute every reference independently** — multi-param reads (`messageId` + `attachmentId`): swap each separately, try `"foo"`/empty/deleted; an ignored parameter is itself the finding.
39. **Issuing-vs-consuming split** — minting endpoint often correct, redeeming endpoint forgotten; test authorization on *both* (`/attachments/{id}`, `/result/{jobId}`, `/download/{token}`).
40. **Stored references inherit data sensitivity + revocation must cover derived tokens** — logged/stored IDs = the data itself; deauthorizing OAuth/session is insufficient if derived bearer IDs stay valid (1+ year here).

### From [[Django Debug Mode to PII Leak (500+ Employees)]]

41. **Random-path DEBUG probe** — garbage path (`/hacker`); yellow page = `DEBUG=True` → hunt `/swagger`, `/redoc`, `/api/docs`, `/openapi.json` (docs travel with debug).
42. **Docs-first discovery + Swagger Authorize with own low-priv JWT** — export `openapi.json`, grep ID-taking endpoints; weakest account + Authorize = whole API clickable; run the IDOR matrix from inside the docs.
43. **Per-subdomain port scan + cross-port token replay** — same subdomain new port = new app; token from surface A replayed on surface B proves shared trust → attack the weaker surface with the stronger surface's sessions.
44. **Open-signup on internal names as its own finding** — `internal/dev/staging/3ntern1l` + public registration = misconfiguration before any IDOR; register and check for shared-backend signals.
45. **Recon pipeline as saved recipe** — `subfinder + amass + assetfinder → sort -u → alterx → httpx -mc 200 → naabu top-ports → nuclei background + manual review parallel` (`alterx` = subdomain permutations, new tool).

### From [[Facebook Analytics Private Chart Disclosure via IDOR]]

46. **Sub-option audit** — Main option (Dashboard Private) protected, Sub-option (Chart info) forgotten; test authz on every nested object independently.
47. **Mutations as read oracles** — Delete/Update mutations echo the full object; a blocked write can still be a successful disclosure.
48. **Parent-path vs direct-node diff** — query nested objects both ways (via parent vs direct global ID); different auth = IDOR.

### From [[Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]]

49. **Friendly-ID swap** — friend/member-only picker → select valid friend for UI, swap to stranger/blocked ID on intercept; any `X_ids[]` param is a candidate.
50. **Bidirectional block matrix** — test `A blocks B`, `B blocks A`, mutual, none; backends often check one direction or neither.
51. **Pending-state as PoC** — attacker-side pending list proves the write even when victim side is blind (blocked); screenshot both sides.
52. **No-reject check as severity lever** — can victim decline/remove? Forced + public + irremovable = MEDIUM, not LOW.

### From [[Facebook Video Poll Deletion via IDOR]]

53. **Delete-array swap** — `deleted_*_ids[]` / `removed_ids[]` params: create own object to pass UI, intercept delete-save, swap to victim child ID; authorize per-element, not per-request.
54. **New-feature first** — freshly shipped sub-tabs (Polls on video) skip security review; hunt the new sub-option before the core flow.
55. **Parent + child independence test** — keep valid owned parent (`v` + `av`), swap only child (`deleted_poll_ids[0]`); valid parent + foreign child succeeding = IDOR.

### From [[Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]]

56. **`/v3/api-docs` first on payment hosts** — unauthenticated docs probe maps `process-payment`, products, `vgNumber`, 3DS before any brute force.
57. **Mint-vs-redeem split for payments** — `/session` (mint) is recon; `/process-payment` (redeem) is the finding; test auth on both independently.
58. **`Origin`-only gate test via curl** — replay sensitive POST with forged `Origin`, no cookies; `200 + side effect` = CORS-as-authz.
59. **Transaction-ID as liveness oracle** — processor-issued ID proves live-infra reach; `200 OK` alone proves nothing.
60. **Payment-session ≠ login-session mental model** — flow context is not identity; don't report step 1 as the vuln.
61. **Ethical payment PoC pattern** — fake token + `H1-RESEARCH-NO-CHARGE` reference + stop at liveness, no PAN/CVV/charge/PII.

### From [[From IDOR to Fraud - Travel Booking Platform bookingId]]

62. **`±1 decrement as first IDOR oracle`** — numeric `?bookingId=` → try `-1/+1` before Intruder; instant `200 + other user data` = fastest BOLA signal.
63. **Twin-endpoint check** — same feature two views (`getbooking` + `getbookingFlight`); one IDOR → test the sibling, shared backend = shared missing check.
64. **Travel-PNR as phishing amplifier** — itinerary (date/route/PNR) makes `your flight X cancelled` phishing zero-guesswork; use it as severity argument, not generic PII.
65. **Proved-vs-possible split** — `proved: mass PII read` + `possible if write endpoints share flaw: ATO/refund`; prevents title overkill, survives triage.

### From [[Live Share Accept Bypass - Regular User Bypasses Admin Approval]]

66. **Accept-side audit (`Invite → Accept/Reject/Cancel/Revoke`)** — test authorization on every post-invite action, not just creation; receiver-side is where RBAC is forgotten.
67. **Email-link as endpoint entry** — follow every invite email with a low-priv session; tokenized link + missing role check = bypass even when UI hides the button.
68. **State-transition BAC framing** — hunt `Pending → Accepted/Approved/Published` moves: `who is allowed to flip this state?` extends BAC beyond IDOR ID-swapping.
69. **Org-scoped write as impact proof** — one low-priv accept → `visible_to_org`; screenshot role proof (Users and Roles) + org-wide result in one PoC to kill triage ambiguity.

### From [[The Missing Link - Broken Access Control to Full ATO]]

70. **"What is the link?" oracle for sequential calls** — Validate-then-Execute (`Authenticate → Set`) with no token/flag/nonce between them = replay step 2 alone. Same-endpoint-twice still counts as two steps.
71. **Generic-update mass-assignment fuzz** — `typeName + entity` / `PUT /profile` endpoints: append `password`, `email`, `role`, `isAdmin`, swap `id` — one variable at a time, harmless field first.
72. **Session-only ATO threat model** — unlocked device / hijacked `sessionId` + missing `oldPassword` check = permanent lockout. State it to justify Critical.
73. **Fresh-login PoC standard** — `200 OK` proves write; incognito login with new credential proves takeover. Always capture both.

### From [[Frontend Security Is Not Enough - Broken Access Control in REST APIs]]

74. **Flash-of-admin-page as BAC signal** — page renders <2s then JS-crashes = guard runs after fetches; read `Fetch/XHR` before the DOM dies.
75. **`301/302` always gets a manual visit** — ffuf redirect on admin-ish path = hidden surface; open it, note pre-crash tabs as endpoint hints.
76. **Fetch-first-then-read timing** — full JS disable kills SPA fetches; keep JS on for the fetch, block only the guard (`Request Blocking` / `window.location` breakpoint). Browser = recon, `curl`/Repeater = proof.
77. **Trust-boundary mental model** — once JSON crosses to the client, JS hiding does not un-send it. Fix is server-side `403` before data, never "JS-first" ordering.

---

## Related
- Full writeup: [[Training Platform - Login Bypass to Full Admin]]
- Full writeup: [[Plan Restriction Bypass - Free Tier to Paid Features]]
- Full writeup: [[Authorization Bypass due to Cache Misconfiguration]] *(todo)*
- Full writeup: [[Authentication Bypass via .php Extension Removal]]
- Full writeup: [[Algolia Search Key Over-Exposure - 154k Records]]
- Full writeup: [[IDOR + Public S3 Report Exposure]]
- Full writeup: [[Easy P3 Broken Access Control - Employee Profile Update]]
- Full writeup: [[Gmail API Attachment IDOR - Missing Object-Level Authorization]]
- Full writeup: [[Django Debug Mode to PII Leak (500+ Employees)]]
- Full writeup: [[Facebook Analytics Private Chart Disclosure via IDOR]]
- Full writeup: [[Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]]
- Full writeup: [[Facebook Video Poll Deletion via IDOR]]
- Full writeup: [[Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]]
- Full writeup: [[From IDOR to Fraud - Travel Booking Platform bookingId]]
- Full writeup: [[Live Share Accept Bypass - Regular User Bypasses Admin Approval]]
- Full writeup: [[The Missing Link - Broken Access Control to Full ATO]]
- Full writeup: [[Frontend Security Is Not Enough - Broken Access Control in REST APIs]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

# Case Study — Simple API Misconfiguration → PII of 100,000+ Users

> **Original write-up:** [Medium — Sagar Kirola](https://medium.com/@sagar_kirola-G35638/how-a-simple-api-misconfiguration-leaked-pii-of-100-000-users-326a1a29bf44)
> **Target:** `target.com` (anonymous, NDA) — all-in-one digital/visual collaboration platform (whiteboards, live quizzes, surveys).
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *auth* vs *authorization*, and *live file* vs *archived file*).

---

## TL;DR

One endpoint with **no per-object authorization** (`GET /manager/api/brainstorms/{board-uuid}/participants`) + **invite links that never expire** + **stale invite codes** recovered from a stray JS file and the Wayback Machine → the PII (emails, names, UUIDs) of **100,000+ users** pulled with a handful of requests. Fixed in under 24 hours, 4-digit bounty.

---

## The Chain (foundation → application)

### 1) The broken endpoint — authentication ≠ authorization
`GET /manager/api/brainstorms/{board-uuid}/participants` returns full details (email, user UUID, first/last name) of **every** participant on a board. The endpoint **requires a login** (you must be a user) but performs **no authorization check** (any participant can query *any* board they can reach).
- **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md|Access Control Types]] — the classic trap: *"is the user authenticated?"* (yes) ≠ *"is the user authorized for THIS object?"* (never checked). The board UUID is the only "key" and it's an object reference, not a permission.

### 2) The twist — invite links never expire
Boards support two invite mechanisms:
1. Direct email invites.
2. A shareable invite link: `https://app.target.com/HTEN234S` — the trailing string (`HTEN234S`) is the invite code, and **these codes never expire**.

> This single design decision is what turned a low-impact flaw into a **mass PII exposure**. A token that never expires is a "time bomb": whatever it grants access to stays reachable forever, even after the token is removed from every live surface.
> - **Foundation:** see the dedicated note on non-expiring tokens in the takeaways below.

### 3) The jackpot — a stray JS file
While reconning beyond the primary app, the researcher found a subdomain: `go.target.com`. Inside it, a JavaScript file — `go.target.com/55932.js` — contained a **hardcoded list of invite codes**. He joined one board from the list and hit the participants API for that board's UUID: **20,000+ users in a single board**, full PII in one request.
- **Foundation:** [[04-Recon/Web Spidering/Intro.md|Spidering/JS enumeration]] + [[07-CheatSheets/Recon.md#JavaScript Enumeration|JS Enumeration]] — old/stray JS bundles leak what the UI never shows. Combined with the authz-less endpoint, the *presence* of a valid code = instant membership = instant participant dump.
- **Key detail:** it doesn't matter *why* the codes were there — hardcoded secrets in static assets are a recon gold mine regardless of intent.

### 4) Scaling the attack — Wayback Machine as a recon tool
Since `go.target.com/55932.js` had been live for a while, he pulled **historical snapshots** of it:
```
https://web.archive.org/web/*/go.target.com/55932.js
```
Older snapshots contained **even more invite codes** that had since been rotated out of the live file — but were still valid (invites never expire).

Then he widened the net with the **Wayback CDX API** over the whole app subdomain:
```
https://web.archive.org/cdx/search/cdx?url=*.app.target.com&fl=original&collapse=urlkey
```
That query surfaced **100+ additional invite codes** scattered across historical snapshots. Joining board after board and repeating the participants call → **100,000+ users** total.
- **Foundation:** full mechanics live in the dedicated recon note → [[04-Recon/Wayback Machine (CDX API).md|Wayback Machine & CDX API]].
- **The insight:** the company *rotated* the codes out of the live file, but rotation only removes them from the *current* surface — the **archive still holds every past version of the same file**. "Deleted" on the live site ≠ deleted in time.

### 5) The requests
```
GET /manager/api/brainstorms/{board-uuid}/participants
Host: app.target.com

# recon
https://web.archive.org/web/*/go.target.com/55932.js
https://web.archive.org/cdx/search/cdx?url=*.app.target.com&fl=original&collapse=urlkey
```

### 6) The check that was missing
The participants endpoint must verify **board membership** (is this requester a participant of *this* board?) server-side per request. It only verified *some* login exists. That single missing check, multiplied by non-expiring invite codes, = 100k PII.

---

## Concept Mapping

- **Vulnerability class:** **Broken access control / IDOR** — the object reference (`board-uuid`) is the only guard; no server-side membership authorization.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md|Access Control Types]]
- **Root cause 1:** Missing authorization (not missing authentication) on the endpoint.
- **Root cause 2:** Non-expiring invite tokens — access credentials that never rotate.
- **Recon technique:** Wayback snapshot browsing + CDX API for historical/secrets recovery.
  → [[04-Recon/Wayback Machine (CDX API).md|Wayback Machine & CDX API]] (dedicated note)
- **Stray JS files as secret sinks:** old assets in unlisted subdomains (`go.target.com`).
  → [[07-CheatSheets/Recon.md#JavaScript Enumeration|JS Enumeration]]
- **Impact scaling:** one broken endpoint + stale-but-valid credentials = mass exposure. The *combination* is what made this Critical.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Authentication ≠ Authorization (as an explicit test step)** — when you find an endpoint you *can* call, ask: "does it check I'm allowed for **this specific object**, or just that I'm logged in?" Swap `board-uuid`/`id` for another object you legitimately access and compare.
2. **Snapshot versioning for rotated secrets** — a token removed from the live file still lives in every Wayback snapshot of that file. Browsing `https://web.archive.org/web/*/<url>` gives you the *full version history* of one asset → collect rotated-out secrets.
3. **CDX API for domain-wide history** — `url=*.domain` + `fl=original` + `collapse=urlkey` = every *distinct* archived URL across time (deduped). Great for finding old JS files, admin pages, backup files. (Full note → [[04-Recon/Wayback Machine (CDX API).md]])
4. **Non-expiring tokens = impact multiplier** — before reporting, check how long the credential stays valid. A token that never expires upgrades any finding it's part of.
5. **Scale = Impact** — the same request on the same endpoint produced 20k → 100k records. Always ask "what's the largest volume this can reach?" before classifying severity.
6. **JS files as invite/reference sinks** — static bundles sometimes contain lists of codes/IDs for purposes only the developer knows. Pulling one gives you a membership credential for free.

---

## Key Takeaways

1. **`Board UUID`/`id` in URL is an object reference, not a permission** — endpoints keyed only by an ID must still verify the requester *owns/participates* in that object.
2. **Login ≠ authorized** — every protected endpoint needs a per-object authorization check, even (especially) when it already requires authentication.
3. **Never-expiring invites are a liability** — codes should have expiry + revocation; otherwise any leak (even a rotated one) stays valid forever.
4. **Rotation is only surface-level** — anything ever public (JS files, pages) is preserved in the Wayback Machine; removing it from the live site doesn't remove it from history.
5. **Stale assets are recon gold** — old subdomains (`go.target.com`) and old JS bundles leak more than the live app ever will.
6. **Combine to escalate** — a "low" authz bug + stale credentials + volume = a Critical PII leak. Judge severity by the *reachable volume*, not the single request.

---

## References

- [How a Simple API Misconfiguration Leaked PII of 100,000+ Users — Sagar Kirola (Medium)](https://medium.com/@sagar_kirola-G35638/how-a-simple-api-misconfiguration-leaked-pii-of-100-000-users-326a1a29bf44)
- Dedicated recon note: [[04-Recon/Wayback Machine (CDX API).md|Wayback Machine & CDX API]]
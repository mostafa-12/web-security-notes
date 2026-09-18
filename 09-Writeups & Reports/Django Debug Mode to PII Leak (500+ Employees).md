# Case Study — From Django Debug Mode to PII Leak of 500+ Employees (BAC + IDOR via Swagger)

> **Original write-up:** [Medium — Aayush Vishnoi (@fa1c0n)](https://medium.com/@fa1c0n/from-django-debug-mode-to-pii-data-leak-of-more-than-500-employees-due-broken-access-control-and-a3eb602a4207)
> **Target:** pentest client — internal subdomain `3ntern1l.redacted.com` on **two ports**: `443` (Login/Sign-Up + dashboard) and `8443` (Django DEBUG mode + Swagger/Redoc API docs)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *port 443 treats the JWT as one user's session* vs *port 8443's API trusts the same JWT for every user's objects*; and *debug/docs meant for developers* vs *exposed to the internet as an attack map*).

---

## TL;DR

Subdomain enum → port scan finds `3ntern1l.redacted.com` on **443 + 8443**. Port 8443 has **Django DEBUG mode on** (yellow debug page on any random path), leaking **Swagger UI + Redoc** docs — a free map of every API endpoint, but the endpoints need an auth token. Port 443 has an **open Sign-Up page** on an internal subdomain → register → steal your own **JWT** from Burp → paste it into Swagger's Authorize button → every protected endpoint becomes clickable → 2–3 endpoints take only an `id` → swap `id` → **PII (names, work emails, phone numbers) of 500+ employees**. Four stacked misconfigurations, one chain.

---

## The Chain (foundation → application)

### 1) Recon pipeline — enum, filter, scan ports, scan vulns
The exact working chain from the write-up (a reusable recipe):

```bash
subfinder -d redacted.com -o subfinder.txt
amass enum --passive -d redacted.com -o amass.txt
echo redacted.com | assetfinder --subs-only | tee assetfinder.txt
cat subfinder.txt amass.txt assetfinder.txt | sort -u | anew subdomains.txt
cat subdomains.txt | alterx | anew subd.txt        # first-time try: permutations
cat subd.txt | httpx -mc 200 | tee live.txt        # who is alive?
cat subd.txt | naabu -top-ports 1000 -o port-scan.txt  # ports per subdomain
# nuclei running in background on live hosts + manual review in parallel
```

> The step most hunters skip is `naabu` **per subdomain**: the find here wasn't a new subdomain — it was a *new port* (`8443`) on an already-known subdomain. → [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]]

### 2) Port 8443 — Django DEBUG mode (the open map room)
`GET https://3ntern1l.redacted.com:8443/hacker` (random string) → Django's yellow **technical 500 debug page** → `DEBUG=True` left on in production. The page listed ~5 endpoints, including **Swagger UI** and **Redoc** dashboards.

> Full deep-dive: [§ Deep-Dive A — Django DEBUG mode](#deep-dive-a--django-debug-mode--why-leaving-it-on-is-critical) and [§ Deep-Dive B — Swagger/Redoc](#deep-dive-b--swagger--redoc--the-free-attack-map) below.

Endpoints visible but **not callable**: every API call needs an Authorization (JWT) the attacker doesn't have yet. The map is free; the keys are not — so the attacker goes looking for a key.

### 3) Port 443 — open Sign-Up on an internal subdomain (the key shop)
Same subdomain on 443 → **Login + Sign-Up pages, registration open**. On a subdomain named `3ntern1l` (internal), open registration is itself a misconfiguration — internal apps should be invite-only / SSO-gated.

Register → log in → dashboard works → Burp history shows the dashboard calling **the same API endpoints** documented in Swagger, each request carrying:

```http
GET /api/employees/123 HTTP/1.1
Host: 3ntern1l.redacted.com
Authorization: Bearer eyJhbGciOi...  (your own low-priv JWT)
```

> Your own token + the public docs = everything needed. No cracking, no theft — just reuse.

### 4) Connecting the two ports — your JWT unlocks Swagger
Copy the JWT from Burp → Swagger UI → **Authorize button** → paste `Bearer <token>` → now every "locked" endpoint in the docs is executable from the browser with your session.

> Why this works is itself a finding — see [§ Deep-Dive C — one infra, two ports](#deep-dive-c--one-infrastructure-two-ports--why-your-443-jwt-worked-on-8443) below.

### 5) The IDOR — endpoints that take only `id`
2–3 endpoints accept a bare `id` parameter. In Repeater (or directly in Swagger's "Try it out"):

```http
GET /api/employees/124 HTTP/1.1
Authorization: Bearer <YOUR_JWT>
→ 200 OK { "first_name": "...", "last_name": "...", "email": "...", "phone": "..." }

GET /api/employees/125 → another employee. 126 → another...
```

Change `id` → someone else's PII. The endpoint verified the JWT is **valid** (AuthN) but never checked `employee.id == request.user.id` or any role gate (AuthZ missing).
→ [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]

**Impact:** first/last names, professional emails, phone numbers of **500+ employees** — enumerable with sequential IDs.

### 6) The missing checks (all four layers)
| # | Layer | Missing check |
|---|-------|---------------|
| 1 | Deploy config | `DEBUG=False` in production; docs endpoints (`/swagger`, `/redoc`) never exposed publicly |
| 2 | Access to internal app | no open Sign-Up on internal subdomain (invite/SSO/IP-allowlist instead) |
| 3 | API authZ | per-object ownership check on every `id`-keyed endpoint |
| 4 | Token scope | one JWT shouldn't unlock admin/internal surfaces across ports (audience/scope separation) |

---

## Deep-Dive A — Django DEBUG Mode — why leaving it on is critical

**What it is:** Django's `DEBUG` setting. When `DEBUG=True` and a request crashes (e.g., an unknown path like `/hacker`), Django renders the famous **yellow technical page** instead of a generic 500.

**Why that page is dangerous — it leaks, by design for developers:**
1. **Full URLconf (every route):** the page lists all URL patterns — the 5 endpoints in this write-up came from here. It's a sitemap the developers wrote for you.
2. **Settings snippet:** parts of `settings.py` context — installed apps, middleware, sometimes DB engine/host, cache and email backends.
3. **Traceback with source code:** surrounding lines of the crashing view, local variable values at each frame — often containing secrets, tokens, query fragments.
4. **Environment + request metadata:** headers, cookies, GET/POST bodies echoed back — useful for session and CSRF analysis.
5. **Interactive console (the nightmare case):** classic Django debug pages (Werkzeug-style in older setups) allow executing Python in the browser when misconfigured — full RCE. Even without it, items 1–4 are enough to plan the whole attack.

**How to detect it (cheap, memorize):**
- Append a random path: `/hacker`, `/xyz123`, `/testtest`. Yellow page = DEBUG on. Generic "Server Error (500)" = off (correct).
- Also try malformed input that crashes views (`?id=[]`, huge ints) — any yellow page confirms it.

**Fix:** `DEBUG=False` + `ALLOWED_HOSTS` set in production (two separate settings, both required); serve docs only in staging behind auth; treat any yellow page on a public host as P1.

## Deep-Dive B — Swagger / Redoc — the free attack map

**What they are:** auto-generated **API documentation UIs** (OpenAPI/Swagger, ReDoc). Developers use them to browse every endpoint, its parameters, and to fire test requests ("Try it out") from the browser.

**Why they're gold for attackers — three properties:**
1. **Completeness:** unlike brute-forced wordlists, docs list *every* endpoint including internal/admin ones nobody links to. The write-up's author never guessed a path — he read them.
2. **Parameter disclosure:** each endpoint shows required params (`id` here) with types and examples — the IDOR targets were labeled.
3. **Built-in exploit console:** the **Authorize** button accepts your JWT once, then every endpoint becomes a point-and-click exploit. No Burp needed for the first pass (use Repeater/Intruder later for scale).

**Relation to DEBUG mode (why they appear together):** frameworks commonly mount docs routes automatically in debug/dev settings (`if DEBUG: urlpatterns += docs_urls`) and teams forget to unmount them in prod. So: **DEBUG page found → immediately probe `/swagger`, `/swagger-ui`, `/redoc`, `/api/docs`, `/openapi.json`, `/api/schema`** — they travel together.

**Hunter workflow when you find docs:**
1. Export `openapi.json` (raw machine-readable spec) — grep it for `id`, `userId`, `email`, `admin`, `password`, `token`.
2. Register the weakest account, paste its JWT into Authorize.
3. Sort endpoints by "takes an object ID" → test IDOR matrix first (yours → other's → `"foo"`/empty/0/-1).
4. Only then look at write endpoints (POST/PUT/DELETE) for BAC.

## Deep-Dive C — One infrastructure, two ports — why your 443 JWT worked on 8443

**The observation:** token minted by the app on **443** was accepted by the API behind **8443**. That is the *proof* both ports share one backend/auth layer.

**What that means architecturally (reconstruction):**
- Same Django project (same `SECRET_KEY` for JWT signing, same user DB) deployed once, served on two ports — e.g., 443 = "public" frontend config, 8443 = dev/debug deployment of the same codebase with `DEBUG=True` and docs mounted.
- Dev-vs-prod separation was done **by port only**, not by infrastructure: same code, same database (500+ real employees reachable from both), same signing key, no audience (`aud`) or scope separation between the two surfaces.

**Why port-only separation fails (the lesson):**
1. Ports are not a security boundary — `naabu` finds them in seconds.
2. The weaker surface (8443: debug + docs, no extra auth) inherits the authority of the stronger one (443: real user DB + valid JWTs).
3. A JWT without `aud`/`scope` claims distinguishing "frontend session" from "internal API" is a master key for every deployment sharing the secret.

**How to test for it anywhere:** whenever two ports/hosts serve the same brand (same login, same JWT shape — compare header/payload on jwt.io):
1. Take a low-priv token from surface A → replay it on surface B's endpoints (docs, debug, admin paths).
2. If accepted → surfaces share trust → attack the weaker surface with the stronger surface's tokens.
3. Also try the reverse (docs-surface token on main surface).

**Fix:** separate secrets/issuers per environment, `aud` + scope claims enforced per surface, docs/debug never deployed with production data, internal surfaces behind SSO/IP-allowlist — never "same app, different port".

---

## Concept Mapping

- **Vulnerability class (primary):** **BOLA / IDOR (horizontal)** — bare `id` parameter, ownership never verified.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]
- **Vulnerability class (secondary):** **missing function-level authorization** — low-priv self-registered user reaches employee-PII endpoints at all (no role gate).
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause stack:** information disclosure (DEBUG + docs) → weak entry (open signup) → missing authz (IDOR). Each layer alone is low; chained = PII of 500+.
- **Recon methodology:** enum → alive-filter → per-subdomain port scan → background vuln scan + manual review in parallel.
  → [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]] + [[07-CheatSheets/Recon.md|Recon]]
- **Tooling:** Burp (history → token theft of *own* session → Repeater ID swap), Swagger UI as first-pass exploit console.
  → [[07-CheatSheets/Burp-Suite.md|Burp Suite]]

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Random-path DEBUG probe** — append garbage (`/hacker`) to any Django-suspect host; yellow page = `DEBUG=True` → immediately hunt `/swagger`, `/redoc`, `/api/docs`, `/openapi.json`.
2. **Docs-first endpoint discovery** — before brute-forcing, export `openapi.json` and grep for ID-taking endpoints; docs beat wordlists because they're complete by construction.
3. **Swagger Authorize with your own low-priv JWT** — weakest account + Authorize button = instant authenticated view of the whole API; sort by `id`-params and run the IDOR matrix from inside the docs.
4. **Per-subdomain port scan (`naabu`)** — same subdomain on a new port is a new app with new settings; always scan top ports per live subdomain, not just the root domain.
5. **Cross-port token replay** — token from surface A on surface B's endpoints; acceptance proves shared trust → attack the weaker surface with the stronger surface's sessions.
6. **Open-signup on internal subdomains as its own finding** — `internal/dev/staging/3ntern1l` + public registration = misconfiguration even before any IDOR; register immediately and look for shared-backend signals (same JWT shape, same data).
7. **Recon pipeline as a saved recipe** — `subfinder + amass + assetfinder → sort -u → alterx → httpx -mc 200 → naabu top-ports → nuclei in background + manual review in parallel`. Save it; reuse it every target. (`alterx` = new tool for this repo: subdomain permutation generation.)

---

## Key Takeaways

1. **DEBUG pages and API docs travel together** — finding one means hunting the other; both mean the deployment was built for developers and shipped to attackers.
2. **Ports are not boundaries** — "dev on 8443, prod on 443" with one DB and one signing key is one trust domain. Test tokens across every surface sharing a brand.
3. **Docs + weakest account = fastest IDOR loop** — no guessing, no brute force for discovery; save Intruder for scale after the first `id` swap hits.
4. **Count the chain, not the bugs** — DEBUG alone is info-leak, signup alone is low, IDOR alone needs a token; together they're 500+ PII records. Report chains show real impact.
5. **Internal names don't mean internal access** — a subdomain called `3ntern1l` reachable from the internet with open signup is public. Verify exposure, never trust the name.

---

## References

- [From Django Debug Mode to PII Data Leak of more than 500+ Employees — Aayush Vishnoi (Medium)](https://medium.com/@fa1c0n/from-django-debug-mode-to-pii-data-leak-of-more-than-500-employees-due-broken-access-control-and-a3eb602a4207)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- IDOR: [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md]]

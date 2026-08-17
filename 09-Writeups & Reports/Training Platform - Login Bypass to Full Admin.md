# Case Study — Login Bypass to Full Admin (Training Platform)

> **Original write-up:** [Medium — Louis Shyers](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently.

---

## TL;DR

Unauthenticated → **write access on 50,000+ user profiles** (5/7 regions) + later SSN leak. Zero credentials, zero payloads. Every bypass = a component-interpretation mismatch.

---

## The Chain (foundation → application)

### 0) Recon — Shodan
`ssl:target.com 200` → internet devices with target SSL cert. Finds assets nothing links to.
- **Foundation:** [[07-CheatSheets/Ports-Services.md#Bug Bounty Notes|Ports & Services]] — hidden ports/services are still found by scanners + Shodan.

### 1) Fingerprinting
Login page discloses **ASP.NET**.
- **Foundation:** [[07-CheatSheets/Recon.md#Technology Fingerprinting|Recon CheatSheet]] — server header, cookies, error pages.

### 2) Directory brute force
`dirsearch` → hit `/ReportServer` → **directory listing enabled** → **SSRS** (SQL Server Reporting Services).
- **Foundation:** [[04-Recon/Discovering Hidden Content/Brute Force.md#Brute-Force Content Discovery|Brute Force]] — guided guessing, not random.

### 3) Bypass #1 — internal hostname swap
Reports redirect to `internal.platform/ReportServer`. Replacing with `platform.com` → loads. The service was exposed; the redirect was just a link, not a control.
- **Foundation:** [[02-Web Architecture/Anatomy of a Web Request.md#3) Trust Boundary|Trust Boundary]] + [[02-Web Architecture/Anatomy of a Web Request.md#6) Platform Misconfiguration|Platform Misconfiguration]] — components trust each other by default.

### 4) First finding (informative)
Report leaking names + user IDs → rejected as **Informative**. Lesson: persistence, not every hit is the win.

### 5) "Content Usage" report = internal site map
Revealed the most-visited endpoints: `platform.com/app/region/<page>.aspx`. Direct access → 401, but the structure fed the next brute-force round.
- **Foundation:** [[04-Recon/Discovering Hidden Content/Methodology.md#2. Start from the Site Map|Start from the Site Map]] + [[04-Recon/Discovering Hidden Content/Brute Force.md#Inference from Published Content|Inference from Published Content]].

### 6) JS reverse-engineering
`scripts/views/courses/index.js` → page built with **Backbone.js**. Because `views/` names = `.aspx` names, predicted `views/users/index.js` → **admin panel code**.
- **Foundation:** [[07-CheatSheets/Recon.md#JavaScript Enumeration|JS Enumeration]] + [[04-Recon/Discovering Hidden Content/Methodology.md#4. Analyze Client-Side Resources|Analyze Client-Side Resources]].

### 7) Reaching admin functionality
`addNewUser()` revealed `Users.aspx/manageUserProfile`. Removing `manageUserProfile` → `Users.aspx/` rendered the **user search page, unauthenticated**.
- **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Phase 2 - Identify Attack Surface|Phase 2 — Identify Attack Surface]] (collect hypotheses, not bugs).

### 8) Bypass #2 — trailing slash
`users.aspx` blocked, `users.aspx/` loads. Canonicalization mismatch between IIS/Akamai layers.
- **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 4 - Try Alternative Requests|Step 4 — Try Alternative Requests]] → URL Manipulation (trailing slash listed there).

### 9) Bypass #2b — double path
Error leaked `Users.aspx/Users.aspx/manageUserProfile` (appended twice). Removing one → **edit-profile page loads**.
- **Foundation:** same [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 4 - Try Alternative Requests|Step 4]] — alternate URL forms.

### 10) Bypass #3 — response manipulation
Form rendered but **client-side read-only**: server sends flag `1`, JS disables fields. Intercept response, change `1 → 0` → editable → **write access, unauthenticated**.
- **Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] (checks in JS ≠ security) + [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md#Never Trust Client-Controlled Data|Never Trust Client-Controlled Data]].

### 11) Scope expansion
Changing `/region/` → **5/7 regions, 50k+ accounts**. Later chained into SSN leak.
- **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Horizontal access controls|Horizontal Access]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 2 - Measure the Scope|Measure the Scope]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 3 - Chain the Vulnerability|Chain the Vulnerability]].

---

## Key Takeaways

1. **One principle, three bypasses** — hostname swap, trailing slash, double path are all the same class: different interpretation of the same request ([[03-Web-Vulnerabilities/temp.md|temp.md]]).
2. **Context-aware recon beats wordlists** — the Content Usage report was the best wordlist.
3. **JS files = admin blueprint** — frameworks are predictable, `views/users/index.js` followed from `Users.aspx`.
4. **Test authorization on every layer** — server AND client (the read-only flag). Client-side checks = broken access control.
5. **Impact = scope, not a single request** — always ask "can I do this to *any* user?"
6. **Informative ≠ dead end** — chain it; value grows with the chain (SSN leak).

---

## References

- [Bypassing a login page and getting full admin access on an internal training platform — Louis Shyers (Medium)](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e)
- Technique credit: Douglas Day — response manipulation (Critical Thinking Bug Bounty podcast)
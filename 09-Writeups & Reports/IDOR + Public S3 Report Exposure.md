# Case Study — IDOR + Broken Access Control → Private Data Exposure via Report Export

> **Original write-up:** [Medium — Ahmed Qaramany (@c0nqr0r)](https://c0nqr0r.medium.com/idor-and-broken-access-control-risking-private-data-exposure-dd808412ed13)
> **Target:** anonymous (NDA) — a platform where users create posts and generate reports for them, with two report-delivery methods: **email** and **PDF export**.
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *ownership check on the API* vs *no authorization on the storage layer*; and *predictable post ID* vs *unguessable job UUID*).

---

## TL;DR

Two chained flaws let any user read **every user's private post reports**: (1) the report-generation API accepts any `postId` **without checking ownership** and returns a `backgroundJobId` (BOLA/IDOR); (2) the generated PDFs live on a public **S3 bucket** reachable through a plain unauthenticated URL. Bruteforcing the sequential post IDs (0 → 9,999,999) mass-collected valid job IDs → full application-wide data exposure.

---

## The Chain (foundation → application)

### 1) The setup — why the tools matter
- **Pwnfox** (Firefox extension): isolates browsing contexts so two test accounts (A and B) never mix sessions — the baseline for any horizontal access control test.
- **Burp Suite**: HTTP History (find the interesting requests), Repeater (manually swap IDs), Intruder (scale to mass enumeration).
- **Autorize** (running in background): replays requests with a swapped/dropped session to flag endpoints that answer *authenticated* requests without a real *authorization* decision. Gives a second set of eyes after manual testing.
- **Obsidian**: a per-app file storing both account IDs, cookies, and any JWT tokens — so every object ID you collect has a home and you never re-derive it.

> Why Obsidian specifically: IDOR testing generates a *lot* of small references (IDs, UUIDs, job IDs, tokens). Keeping them in a searchable graph note lets you connect them later (e.g., `postId` → `backgroundJobId` → `downloadUrl`).

### 2) Mapping the surface — click every button
The platform allows full **CRUD** on posts. The write-up stresses that access control was *"not well enforced across the board"* — so every operation is a candidate. Then a report feature shows up:

- **First idea — report by email:** change the `postId` hoping to get someone else's report emailed to you.
- **Result:** the report was sent to the **email bound to the account (server-side)** — the recipient can't be redirected from the request. Looked "secure."

> **The subtle lesson here:** the app fixed the *recipient* (bound it server-side) but **never fixed the ownership check**. The email path *seemed* safe, but the same missing check was waiting in the PDF path. → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md|Access Control Types]] (horizontal access control)

### 3) The PDF export — an async background job (two requests)
When you click "Export as PDF" the app doesn't return the file synchronously. It spawns a **background job** and returns a reference to it:

```
POST /api/reports/generate
Cookie: session=...
Body: { "postId": 12345 }

Response:
{ "backgroundJobId": "d69047b7-3a7a-4784-96be-6633b6d8bd45", "status": "CREATED" }
```

Then a second request polls the job / fetches its output:

```
GET /api/reports/result/{backgroundJobId}

Response:
{ "status": "COMPLETED", "downloadUrl": "https://s3.amazonaws.com/companyname/report/20241013/d69047b7-3a7a-4784-96be-6633b6d8bd45.pdf" }
```

> **Why two requests matter for testing:** the *job reference* (`backgroundJobId`) and the *actual file URL* live on **different layers**. Each layer must be tested separately: "Can I get a job for someone else's post?" (request 1) and "Can I fetch a job result that isn't mine?" (request 2). → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]] (Phase 3 — test the authorization decision on *every* step of a workflow)

### 4) The IDOR — the job ID is not your property
Send Request 1 to **Repeater**, swap `postId` to another user's post → the server still returns a **valid `backgroundJobId`**.

- The check that should exist: `post.owner == session.user` **before** creating the job.
- It's **not** checked. → classic BOLA/IDOR: the object reference (`postId`) is the *only* guard, and it's client-controlled. → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + Lab: [[03-Web-Vulnerabilities/Access control vulnerabilities/Labs/10-Insecure direct object reference.md|10-Insecure direct object reference]]

### 5) Scaling — sequential IDs + Intruder
Posts use **sequential numeric IDs**. So:

1. Send Request 1 to **Intruder**, position the payload on `postId`.
2. Range: **0 → 9,999,999**.
3. Grep the responses for valid `backgroundJobId`s.
4. Collect other users' job IDs → repeat the download for each.

> ⚠️ **Scope/responsibility gap in the original write-up:** a 10-million-request brute force is a resource hit on the target and mass data harvesting. Programs often forbid this. Prove impact on a handful of IDs; don't enumerate everything.

### 6) The storage layer — the real severity driver
The `downloadUrl` is a **plain S3 URL — no signature, no token, no auth**. Anyone who knows the path downloads the file. Two sub-cases to test (full mechanics → [[11-Infrastructure/Amazon S3.md|Amazon S3]]):

| Exposure level | How to reach the data | Severity |
|---|---|---|
| **Objects public-read** (this report) | Need the `backgroundJobId` (from the IDOR above) | High |
| **Bucket also allows `ListBucket`** | Enumerate **every** key with no prior knowledge — UUIDs become irrelevant | Critical |

In this write-up the bucket was at least object-public; whether it also allowed listing isn't stated — but it's the **first thing to check** on any `s3.amazonaws.com/...` URL you see.

### 7) The missing checks (summarized)
- **API layer:** validate ownership before generating a job for a `postId`.
- **Result layer:** validate the `backgroundJobId` belongs to the requester.
- **Storage layer:** private bucket + short-lived **presigned URLs** scoped per user.

> Defense in depth: each layer must be independently secure. The write-up's own framing ("UUIDs are not enough") is imprecise — the UUID is fine; what's missing is authorization at **every** step. → [[02-Web Architecture/Anatomy of a Web Request.md|Trust Boundary & Platform Misconfig]]

---

## Concept Mapping

- **Vulnerability class (primary):** **BOLA / IDOR (horizontal access control)** — the `postId` object reference is client-controlled and ownership is never verified.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Horizontal access controls|Horizontal access control]]
- **Vulnerability class (secondary):** **missing authorization at the storage layer** — the S3 bucket serves private files to anyone who knows the URL; no presigned URL, no per-request check.
  → [[11-Infrastructure/Amazon S3.md|Amazon S3]]
- **Root cause:** *auth ≠ authz* at two different layers (API + storage). The app authenticated you for the feature but never authorized you for the *object*.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md|Access Control Testing Methodology]] — "every protected endpoint needs a per-object authorization check"
- **Async job pattern as attack surface:** a workflow split across two requests means authorization must be enforced on *each* step, not once.
  → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]]
- **Enumeration technique:** sequential IDs + Intruder = scale a single IDOR into mass data exposure.
  → [[04-Recon/Discovering Hidden Content/Brute Force.md|Guided Brute Force]]
- **Tooling:** Burp (History → Repeater → Intruder) + Autorize for background authz scanning + Pwnfox for session isolation.
  → [[07-CheatSheets/Burp-Suite.md|Burp Suite]]

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Async background-job pattern as an IDOR surface** — when a feature returns a "job reference" (`backgroundJobId`, `taskId`, `requestId`) instead of the result, test *both* requests: the one that creates the job (swap the object ID) and the one that fetches the result (is the job ID yours?). Authorization must be enforced at every step of the workflow.
2. **Two-request report pipelines** — email + PDF export for the same data are two independent surfaces. Testing one "secure" path (email recipient bound server-side) doesn't prove the other is safe — the same missing check can live elsewhere.
3. **File-storage URLs are a storage-layer boundary, not an API one** — a `downloadUrl` on S3/cloud storage is a *different trust domain* than the API that produced it. Test it on its own: plain URL vs presigned, object-public vs list-public.
4. **UUIDs are references, not permissions** — unguessable ≠ authorized. A UUID is only as good as the *narrowest* way to obtain it; if any endpoint hands it out without ownership checks, its secrecy is gone. (And you never brute-force a UUID — you brute-force whatever *sequential* ID sits in front of it.)
5. **`?list-type=2` / `--no-sign-request` as a storage oracle** — on any `s3.amazonaws.com/<bucket>/...` URL, test whether the bucket also allows listing (anonymous list = the whole dataset with zero knowledge).
6. **Respect scope on enumeration** — a 0→10M brute force proves "all posts are exposed" but can get you banned/fined. Prove impact with a few IDs and state that full enumeration is possible.

---

## Key Takeaways

1. **Object references (post ID, job ID, UUID) are never a permission** — every endpoint keyed by an ID must verify the requester is allowed to touch *that* object, server-side, per request.
2. **Auth ≠ authz, at every layer** — the app authenticated the user but never authorized the *object*; then it repeated the same mistake on the storage layer.
3. **A fixed symptom ≠ a fixed root cause** — binding the email recipient server-side didn't fix the missing ownership check; it just moved the bug to a different delivery path.
4. **Security through obscurity fails when there's a leak path** — the UUID is unguessable, but the predictable `postId` in front of it made it obtainable. Never rely on ID entropy instead of authorization.
5. **Storage misconfiguration multiplies severity** — the API bug alone exposes reports you have job IDs for; a public/listable bucket exposes *everything* to *anyone*.
6. **Test the whole workflow** — multi-request features (async jobs, multi-step workflows) need an authorization test on *each* step, not just the first response that looks interesting.

---

## References

- [IDOR and Broken Access Control Risking Private Data Exposure — Ahmed Qaramany (Medium)](https://c0nqr0r.medium.com/idor-and-broken-access-control-risking-private-data-exposure-dd808412ed13)
- Dedicated storage note: [[11-Infrastructure/Amazon S3.md]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
# 09-Writeups & Reports

## Purpose

Real-world case studies from bug bounty write-ups. Each write-up is broken down stage-by-stage, mapped to the concepts already documented in this repo, and mined for techniques that the detailed notes don't cover yet.

The goal is not to copy reports — it's to see how the methodology in this repo plays out in the wild, and to extract the gaps that need their own notes.

---

## Contents

| File | Topic |
|------|-------|
| `Reports Summary Table.md` | Compact table (link, idea, tip, vuln param, vuln method, impact) for every report + Q&A + new techniques learned |
| `Training Platform - Login Bypass to Full Admin.md` | Shodan recon → SSRS ReportServer → JS reverse-engineering → 3 access-control bypasses → write access on 50k+ accounts. [Original write-up (Medium)](https://medium.com/@l_s_/bypassing-a-login-page-and-getting-full-admin-access-on-an-internal-training-platform-ff5abd88135e) |
| `Plan Restriction Bypass - Free Tier to Paid Features.md` | UI hides a paid feature → backend never enforces the plan → crafted URL + `PUT /api/0/projects/.../plugins/splunk/` gives free-tier users data-forwarding (paid). $469 bounty. Target: [[10-Targets/Sentry\|Sentry]]. [Original write-up (Medium)](https://medium.com/h7w/how-i-earned-469-bounty-bypassing-plan-restriction-58f6d3120b6e) |
| `Authorization Bypass due to Cache Misconfiguration.md` *(todo)* | Micro-caching → auth NOT in cache key → any user fetches any shop's orders in the 3–4s window. [Original write-up (Medium)](https://rikeshbaniya.medium.com/authorization-bypass-due-to-cache-misconfiguration-fde8b2332d2d) |
| `API Misconfiguration - PII Leak (100k users).md` | Participants API checks *auth* but never *authorization* + non-expiring invite links + stale codes from a stray JS file & Wayback CDX → PII of 100k+ users. [Original write-up (Medium)](https://medium.com/@sagar_kirola-G35638/how-a-simple-api-misconfiguration-leaked-pii-of-100-000-users-326a1a29bf44) |
| `Algolia Search Key Over-Exposure - 154k Records.md` | Over-permissioned Algolia search key → internal financial fields, moderation-status filtering, a second index (~80k), gender-identity facets + leaked `server.js.map` (2nd dev key + anti-bot bypass). Re-tested an old "Resolved" duplicate → still live → High severity. [Original write-up (Medium)](https://medium.com/@Tyrion404/from-duplicate-to-bounty-88d6511dc6db) |
| `IDOR + Public S3 Report Exposure.md` | Report generation = async background job: `postId` → `backgroundJobId` (ownership never checked) → PDF on a public S3 bucket, plain unauthenticated URL. Sequential post IDs + Intruder (0→9,999,999) → all users' private reports exposed. [Original write-up (Medium)](https://c0nqr0r.medium.com/idor-and-broken-access-control-risking-private-data-exposure-dd808412ed13) |
| `From Internal User to Admin - Broken Access Control in SaaS.md` | UI hides role selector for Internal Users; backend accepts `companyUserRoles` on `/contacts` without authz check → Internal User invites Manager/Administrator accounts. Closed as duplicate. [Original write-up (Medium)](https://medium.com/@mobadawyx4/from-internal-user-to-admin-exploiting-broken-access-control-in-saas-platforms-c1a2e36489a4) |
| `Easy P3 Broken Access Control - Employee Profile Update.md` | Employee profile shown read-only in UI; backend update endpoint accepts replayed request from low-priv session → profile name changed to HACKED. Triaged then duplicate. [Original write-up (Medium)](https://medium.com/@a0xtrojan/easy-p3-broken-access-control-7c28702cb1ee) |
| `Gmail API Attachment IDOR - Missing Object-Level Authorization.md` | `users.messages.attachments.get` returns any attachment for any valid `attachmentId` (`messageId` ignored, even `"foo"` works) — any authenticated Google user reads anyone's attachments. Reported Jan 2023, fixed by Google. [Original write-up (Material Security)](https://material.security/resources/how-material-security-uncovered-a-vulnerability-in-the-gmail-api) |
| `Django Debug Mode to PII Leak (500+ Employees).md` | Internal subdomain on 443 (open Sign-Up) + 8443 (Django DEBUG + Swagger/Redoc) sharing one backend → own low-priv JWT in Swagger Authorize → bare-`id` endpoints → PII of 500+ employees. Includes deep-dives: Django DEBUG dangers, Swagger as attack map, cross-port token reuse. [Original write-up (Medium)](https://medium.com/@fa1c0n/from-django-debug-mode-to-pii-data-leak-of-more-than-500-employees-due-broken-access-control-and-a3eb602a4207) |
| `Authentication Bypass via .php Extension Removal.md` | Wildcard subdomain → SVG source path → custom 404 leaks app UI → `/videos.php` auth → `/videos` bypass → all user videos + `/media/` directory listing. Zero creds, zero payloads. |
| `jwt-design-flaw-scenario.md` | Refresh JWT as sole source of truth (signature-only, no `jti`/session/rotation) → stolen token = zero-click takeover until expiry. Includes vulnerable vs fixed (session store + rotation + reuse detection) pseudo-code. Related: `02-Web Architecture/Access & Refresh Tokens.md`. |

---

## Structure of Each Case Study

1. **Scenario Walkthrough** — every stage with the actual technique used.
2. **Concept Mapping** — what it teaches, linked to the repo notes that already cover it.
3. **New Techniques** — skills in the write-up that this repo doesn't document yet (future note candidates).
4. **Key Takeaways** — the reusable lessons, not the specific payloads.

---

## Related Notes

- `03-Web-Vulnerabilities/temp.md` — the core principle: two components interpreting the same data differently
- `03-Web-Vulnerabilities/Access control vulnerabilities/` — access control types, testing methodology, labs
- `04-Recon/Discovering Hidden Content/` — recursive content discovery, context-aware brute force
- `07-CheatSheets/Recon.md` — recon quick reference

---

## Study Order

```
1. Read the vulnerability notes first (Access Control methodology + Recon).
2. Then read the case study and try to predict each bypass before reading it.
3. Extract the "New Techniques" sections and add them to the detailed notes as you study them.
```
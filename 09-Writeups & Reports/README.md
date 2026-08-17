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
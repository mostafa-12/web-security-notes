# 07-CheatSheets

## Purpose

Quick-reference documents for web security testing. Each sheet covers a single topic — HTTP, authentication, access control, Burp Suite, etc. — designed for fast lookup during labs and bug bounty hunting.

---

## Contents

| File | Topics |
|------|--------|
| `HTTP.md` | Methods, Content Types, GET vs POST, PUT vs PATCH, Cookies, HTTPS, REST |
| `Status-Codes.md` | 1xx–5xx with testing relevance, 401 vs 403, anomalies |
| `Useful-Headers.md` | Request/Response/Security/Auth/Caching/Proxy headers |
| `Authentication.md` | Auth flow, MFA, OAuth, SSO, common weaknesses, login checklist |
| `Session-Management.md` | Session lifecycle, JWT (structure + bugs), fixation, hijacking, SameSite |
| `Access-Control.md` | Vertical/Horizontal escalation, IDOR, forced browsing, 403 bypass |
| `Input-Validation.md` | Whitelist/Blacklist, canonicalization, output encoding, parameterized queries |
| `Burp-Suite.md` | Every tool (Proxy, Intruder, Repeater...), shortcuts, professional workflow |
| `Recon.md` | Application mapping, spidering, robots.txt, backup files, JS/API discovery |
| `Encoding.md` | URL, HTML, Unicode, Base64, Hex, JSON, double encoding, bypass techniques |
| `Notes-To-Remember.md` | Core principles, common pitfalls, bug bounty mindset |

---

## Related Notes

- `01-HTTP/` — Detailed HTTP notes (foundation for all cheat sheets)
- `04-Recon/` — In-depth reconnaissance methodology
- `02-Web Architecture/` — Architecture concepts

---

## Study Order

```
1.  HTTP.md
2.  Status-Codes.md
3.  Useful-Headers.md
4.  Encoding.md
5.  Authentication.md
6.  Session-Management.md
7.  Access-Control.md
8.  Input-Validation.md
9.  Burp-Suite.md
10. Recon.md
11. Notes-To-Remember.md
```

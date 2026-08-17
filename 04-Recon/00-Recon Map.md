# 04-Recon — Content Map

## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Content Index](#content-index)
- [Related Content in Other Folders](#related-content-in-other-folders)
- [Study Order](#study-order)

---

## Overview

> Reconnaissance is the process of mapping a target application's attack surface before testing. Every finding starts with good recon.

---

## Folder Structure

```
04-Recon/
├── Manual Browsing.md
├── Robots file.md
├── Site Map.md
├── Web Spidering/
│   ├── Intro.md
│   ├── User Spidering Methodology (WAHH).md
│   ├── Site Map Discovery vs Crawling.md
│   └── Per-Page CSRF Tokens Limitations.md
├── Discovering Hidden Content/
│   ├── Intro.md
│   ├── Methodology.md
│   ├── Brute Force.md
│   ├── Context-Aware WordList.md
│   └── Other Resources to Site's content.md
└── Wayback Machine (CDX API).md
```

---

## Content Index

### Recon Fundamentals

| File                 | Topic                   | Key Takeaway                                      |
| -------------------- | ----------------------- | ------------------------------------------------- |
| `Manual Browsing.md` | Manual browsing process | First step — understand the application as a user |
| `Robots file.md`     | robots.txt              | Not a security control — may reveal hidden paths  |
| `Site Map.md`        | HTML & XML sitemaps     | robots.txt vs sitemap.xml comparison              |

### Web Spidering

| File                                                 | Topic                  | Key Takeaway                                      |
| ---------------------------------------------------- | ---------------------- | ------------------------------------------------- |
| `Web Spidering/Intro.md`                             | Spidering fundamentals | How automated crawling works + limitations        |
| `Web Spidering/User Spidering Methodology (WAHH).md` | WAHH methodology       | 4-step approach: proxy → browse → review → spider |
| `Web Spidering/Site Map Discovery vs Crawling.md`    | Discovery vs crawling  | Discovered URL ≠ Crawled URL                      |
| `Web Spidering/Per-Page CSRF Tokens Limitations.md`  | CSRF token issues      | How per-page tokens break automated spidering     |

### Hidden Content Discovery

| File | Topic | Key Takeaway |
|------|-------|--------------|
| `Discovering Hidden Content/Intro.md` | What is hidden content | Files/resources with no incoming links |
| `Discovering Hidden Content/Methodology.md` | Discovery methodology | Recursive enumeration + functional path model + hidden parameters (largest file) |
| `Discovering Hidden Content/Brute Force.md` | Brute force discovery | Guided guessing, not random — naming conventions + numeric patterns |
| `Discovering Hidden Content/Context-Aware WordList.md` | Smart wordlists | Wordlists based on app structure, not generic lists |
| `Discovering Hidden Content/Other Resources to Site's content.md` | Public info recon | Search engines, Wayback Machine, developer footprints, people-based recon, web server |

### Historical Recon (Wayback Machine)

| File | Topic | Key Takeaway |
|------|-------|--------------|
| `Wayback Machine (CDX API).md` | Archived snapshots & CDX API | Rotation is surface-level — old snapshots still hold rotated-out secrets; CDX API enumerates every URL the domain ever had |

---

## Related Content in Other Folders

### `07-CheatSheets/Recon.md`

> **Quick reference version of everything in this folder.**

Covers: Application Mapping, Manual Browsing, Spidering, robots.txt, Backup Files, Directory Discovery, JavaScript Enumeration, API Discovery, Technology Fingerprinting, What to Record.

Use this as a **fast lookup** while the detailed notes live here.

---

### `07-CheatSheets/Burp-Suite.md`

| Section | Related To |
|---------|-----------|
| **Proxy** | Intercepting traffic during manual browsing |
| **Target** | Site Map review, scope definition |
| **Repeater** | Manual testing of discovered endpoints |
| **Intruder** | Directory brute forcing, parameter discovery |
| **HTTP History** | Reviewing captured traffic for hidden endpoints |
| **Logger** | Background traffic discovery |

---

### `07-CheatSheets/Status-Codes.md`

| Section | Related To |
|---------|-----------|
| **200 OK** | May be a custom 404 page (hidden content returns 200) |
| **403 Forbidden** | Access control bypass testing |
| **405 Method Not Allowed** | Reveals allowed HTTP methods |
| **429 Too Many Requests** | Rate limiting during brute force |

---

### `07-CheatSheets/Useful-Headers.md`

| Section | Related To |
|---------|-----------|
| **Server / X-Powered-By** | Technology fingerprinting |
| **X-Forwarded-For / X-Original-URL** | 403 bypass during hidden content discovery |
| **Cache-Control** | Cached content may reveal hidden pages |

---

### `07-CheatSheets/Access-Control.md`

| Section | Related To |
|---------|-----------|
| **Forced Browsing** | Accessing hidden pages directly |
| **Vertical Privilege Escalation** | Discovering admin endpoints |
| **IDOR** | Discovered endpoints with predictable IDs |

---

### `07-CheatSheets/Encoding.md`

| Section | Related To |
|---------|-----------|
| **URL Encoding** | Bypassing directory brute force filters |
| **Double Encoding** | Bypassing input validation during discovery |
| **Base64** | Decoding discovered tokens in JS/API responses |

---

### `01-HTTP/Proxy.md`

> Detailed explanation of how Burp Proxy works (MITM, TLS, certificate pinning).

Related to: Intercepting traffic during manual browsing and spidering.

---

### `01-HTTP/Messages.md`

> HTTP Request/Response structure.

Related to: Understanding what you see in Burp during recon.

---

### `02-Web Architecture/Mapping Methodology.md`

> 7-step methodology for mapping attack surface.

Related to: Application Mapping phase of recon.

---

### `02-Web Architecture/Ajax.md`

> How Ajax works, XHR/Fetch, DOM updates.

Related to: Spidering limitations with Ajax-heavy applications.

---

### `08-Python Automating Project (ideas)/Web-Spidering-py.md`

> Python web spidering project idea (OWASP Juice Shop).

Related to: Automating the spidering process.

---

## Study Order

```
1. Manual Browsing.md
   └── Understand the app as a user first

2. Robots file.md + Site Map.md
   └── Static reconnaissance

3. Web Spidering/Intro.md
   └── How automated crawling works

4. Web Spidering/User Spidering Methodology (WAHH).md
   └── The recommended approach

5. Web Spidering/Site Map Discovery vs Crawling.md
   └── Understanding the workflow

6. Web Spidering/Per-Page CSRF Tokens Limitations.md
   └── Common spidering pitfall

7. Discovering Hidden Content/Intro.md
   └── What is hidden content

8. Discovering Hidden Content/Methodology.md
   └── Core methodology (read carefully)

9. Discovering Hidden Content/Brute Force.md
   └── Guided enumeration

10. Discovering Hidden Content/Context-Aware WordList.md
    └── Smart wordlists

11. Discovering Hidden Content/Other Resources to Site's content.md
    └── Public info recon

12. Wayback Machine (CDX API).md
    └── Historical recon — rotated secrets + domain-wide URL discovery

Then: 07-CheatSheets/Recon.md (as quick reference)
```

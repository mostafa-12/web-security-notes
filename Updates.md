 
# Learning Log

---

## 2026-07-21

### Completed

#### Linux (Linux Journey — Grasshopper)

- ✅ Linux History — UNIX, GNU Project, Linux Kernel
- ✅ Command Line — Shell vs Terminal, Bash, Shell Prompt, Command Structure
- ✅ Commands — pwd, cd, ls, touch, file, cat, less, history, cp, mv, mkdir, rm, find, help, man, whatis, alias, exit

#### Recon (WAHH)

- ✅ Manual Browsing — process, multi-step workflows, limitations
- ✅ Robots.txt — how it reveals hidden directories
- ✅ Site Maps — HTML vs XML sitemaps, robots.txt vs sitemap.xml
- ✅ Web Spidering — fundamentals, user-directed spidering methodology (WAHH), discovery vs crawling, CSRF token limitations
- ✅ Hidden Content Discovery — intro, methodology (recursive enumeration), functional path model, hidden parameters, brute force, context-aware wordlists, public info recon (search engines, Wayback Machine, developer footprints, people-based recon, web server exploitation)

---

### 💡 Key Concepts I Finally Understood

- The difference between Terminal, Shell, and Kernel — and how they work together.
- Shell is a command interpreter, not the same as Terminal.
- Linux = GNU Tools + Linux Kernel (GNU/Linux).
- Hidden content discovery is an iterative process — every discovery guides the next round.
- A discovered URL is not the same as a crawled URL.
- Brute-force content discovery is guided, not random — it follows naming conventions and application structure.
- Functional path model: some apps expose all functionality through a single endpoint where parameters determine the function, not the URL.
- robots.txt is a guide for crawlers, not a security control — it may reveal sensitive paths.

---

### 🛠 Repository Improvements

- Added `05-Linux/` section with Intro and comprehensive Command Line notes.
- Added `04-Recon/` section with 12 files covering manual browsing, spidering, and hidden content discovery.
- Added `02-Web Architecture/Mapping Methodology.md`.

---

## 2026-07-14

###  Completed

#### Web Application Hacker's Handbook

- ✅ Chapter 3 — Web Application Technologies

#### MDN HTTP

Studied and documented:

- HTTP Messages
- HTTP Methods
- HTTP Headers
- Status Codes
- Cookies
- Cookie Attributes
- SameSite
- Cookie Prefixes
- Privacy & Tracking
- HTTPS
- Proxy Authentication
- State & Sessions
- DOM
- Ajax
- JSON
- Encoding Schemes

---

### 💡 Key Concepts I Finally Understood

- How Burp Proxy performs a Man-in-the-Middle attack using two independent TLS connections.
- Why Burp generates its own certificate instead of reusing the server's certificate.
- Why Certificate Pinning breaks Burp interception.
- Difference between a Session and a Session ID.
- How SameSite mitigates CSRF attacks.
- Why `__Host-` cookies help prevent Session Fixation.
- Difference between First-Party and Third-Party Cookies.
- HTTP/2 changes the transport format (binary framing), not HTTP semantics.

---

### 🛠 Repository Improvements

- Reorganized the HTTP notes into dedicated topics.
- Split Cookies into multiple focused notes:
  - Attributes
  - SameSite
  - Cookie Prefixes
- Added an HTTP knowledge base structure.
- Improved note organization for future expansion.

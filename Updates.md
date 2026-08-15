 
# Learning Log

---

## 2026-08-15

### Completed

#### Networking

- ✅ Network Basics — network types (LAN/WAN), physical vs logical, topologies (Bus, Ring, Star, Mesh, Partial-Mesh), cables (Coaxial, Twisted-Pair, Fiber), access methods (CSMA/CD)
- ✅ OSI 7 Layers — layer-by-layer notes, adjacent vs same-layer interactions, presentation/session/transport behavior, duplex modes & auto-negotiation
- ✅ Connection Models — Work Group (P2P) vs Client/Server (Domain): local vs centralized accounts, how permissions work in each, Share vs NTFS permissions

#### IP Configuration (DHCP)

- ✅ Ports & Sockets — port ranges (0-1023, 1024-49151, 49152-65535), socket = IP + Port, socket vs port, relation to web security
- ✅ How a device gets an IP — Manual (Static), DHCP, Alternate Configuration, APIPA (169.254.x.x)
- ✅ DORA — Discover/Offer/Request/Acknowledge, why each step is broadcast vs unicast, why REQUEST must be broadcast, when broadcast is not needed (renewal, DHCP relay)

#### DNS

- ✅ DNS workflow — key terms (FQDN, Resolver, Root/TLD/Authoritative servers, A/AAAA, CNAME, TTL, Cache), resolution flow, Recursive vs Iterative queries

#### Access Control (continued)

- ✅ Completed remaining Access Control labs (10–12):
  - IDOR (Insecure Direct Object Reference)
  - Multi-Step Process Access Control
  - Referer-Based Access Control
- ✅ IDOR note + Referer-Based Access Control note

#### Repository Improvements

- ✅ Created `06-Networking/` section (Basics, Intro, OSI 7 layer folder)
- ✅ Filled `Connection Models.md`, `Ports.md`, expanded `Application Layer-TCP-IP.md` (DHCP + DNS)
- ✅ Added `07-CheatSheets/Ports-Services.md` + updated CheatSheets README

---

### 💡 Key Concepts

- Permissions in P2P are local to each device — a user account does not propagate to other machines
- DORA broadcast vs unicast depends on what the client knows: no IP + unknown server → broadcast; known server → unicast
- APIPA (169.254.x.x) is a fallback symptom, not a real network configuration
- DNS is hierarchical — no single server knows everything, resolution walks Root → TLD → Authoritative

---

### Next Goal

- Continue Access Control testing methodology practice
- Start CORS attack scenarios / next vulnerability class
- Continue Linux + Networking roadmap topics

---

## 2026-07-29

### Completed

#### Access Control

- ✅ Access Control Types — Vertical, Horizontal, Context-Dependent
- ✅ Access Control Testing Methodology — 4-phase methodology (Understand → Identify → Test → Validate)
- ✅ 9 PortSwigger Access Control labs (00–09):
  - Unprotected admin functionality
  - Unprotected admin with unpredictable URL
  - User role controlled by request parameter
  - User role modified in user profile
  - URL-based access control circumvented
  - Method-based access control circumvented
  - User ID controlled by request parameter (regular, unpredictable user IDs, data leakage in redirect, password disclosure)

#### Web Architecture

- ✅ Anatomy of a Web Request — Browser → DNS → TCP → TLS → Reverse Proxy → Gunicorn → Middleware → Flask
- ✅ Trust Boundary analysis — which components trust each other, where attackers can inject
- ✅ Platform Misconfiguration — how different components can interpret the same request differently (X-Original-URL, X-Rewrite-URL)

#### Repository Improvements

- Stripped CheatSheets of topics not actually studied (OAuth, SSO, IDOR section, JWT internals, SQLi/XSS examples, tools/wordlists)
- Fixed `Updates.md` entry format for consistency with the 2026-07-14 style
- Aligned all CheatSheet content with existing detailed notes only

---

### Key Concepts

- Authorization belongs inside the application, not just at the infrastructure layer
- Different components interpreting the same request differently is the root cause of many access control bypasses
- Never trust metadata (headers) unless you know who generated it — one component's internal header can be another component's attack vector
- Access control testing is hypothesis-driven: observe first, build theories, then verify

---

### Next Goal

- Start IDOR (Insecure Direct Object References) labs
- Continue with CORS — study the mechanism and attack scenarios
- Continue PortSwigger Access Control labs (remaining labs)

---

## 2026-07-21

### Completed

#### CheatSheets

- ✅ Created `07-CheatSheets/` — 11 quick-reference cheat sheets based on all studied topics
- ✅ Created `04-Recon/00-Recon Map.md` — navigation file linking recon content across the repo
- ✅ Added README navigation to `01-HTTP/`, `04-Recon/`, `05-Linux/`, and `07-CheatSheets/`

#### CheatSheets Created

- HTTP — methods, content types, cookies, REST
- Status-Codes — 1xx–5xx with testing relevance
- Useful-Headers — request, response, security, auth, caching, proxy headers
- Authentication — flow, common weaknesses, checklist
- Session-Management — lifecycle, cookies, JWT, fixation, hijacking
- Access-Control — vertical, horizontal, forced browsing, context-dependent
- Input-Validation — whitelist vs blacklist, canonicalization, output encoding
- Burp-Suite — every tool, workflow, shortcuts
- Recon — phases, mapping, spidering, directory discovery, JS/API
- Encoding — URL, HTML, Unicode, Base64, Hex, JSON, double encoding
- Notes-To-Remember — core principles, pitfalls, mindset

---

### 💡 Key Concepts

- Cheat sheets are quick references, not replacements for detailed notes
- Every cheat sheet follows the same structure: tables, bug bounty notes, common mistakes, checklist
- Recon folder now has a map file connecting it to related content across the repo

---

### 🛠 Repository Improvements

- Added `07-CheatSheets/` section with 11 cheat sheets
- Added `04-Recon/00-Recon Map.md` for cross-folder navigation
- Added README.md to `01-HTTP/`, `04-Recon/`, `05-Linux/`

---

### 📖 Next Goal

- Chapter 4 — The Web Application Hacker's Handbook
- Begin studying **Access Control**
- Start solving PortSwigger Access Control labs alongside the theory

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

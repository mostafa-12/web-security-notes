# Recon CheatSheet

## Table of Contents

- [Overview](#overview)
- [Recon Phases](#recon-phases)
- [Application Mapping](#application-mapping)
- [Manual Browsing](#manual-browsing)
- [Spidering](#spidering)
- [robots.txt & sitemap.xml](#robotstxt--sitemapxml)
- [Backup Files](#backup-files)
- [Directory Discovery](#directory-discovery)
- [JavaScript Enumeration](#javascript-enumeration)
- [API Discovery](#api-discovery)
- [Technology Fingerprinting](#technology-fingerprinting)
- [What to Record](#what-to-record)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Recon is the foundation of web security testing. Better recon = better findings. Most missed bugs are due to incomplete recon.

---

## Recon Phases

```
Phase 1: Passive Recon
  → WHOIS, DNS, Subdomains, certificates, public info

Phase 2: Application Mapping
  → Manual browsing, spidering, site map, technology fingerprinting

Phase 3: Content Discovery
  → Hidden files, directories, parameters, endpoints

Phase 4: Vulnerability Analysis
  → Testing identified attack surface
```

---

## Application Mapping

| Step | Description |
|------|-------------|
| 1. Identify entry points | URLs, parameters, headers, cookies |
| 2. Fingerprint technologies | Framework, language, server, CMS |
| 3. Infer server-side behavior | URL structure, parameters, file extensions |
| 4. Look for inconsistencies | Legacy code, different naming, third-party plugins |
| 5. Prioritize attack surface | Auth, admin, upload, API, payment |

---

## Manual Browsing

> Browse the application like a normal user — then like an attacker.

### Process

```
1. Start from homepage
2. Follow every link
3. Complete every multi-step workflow
4. Try different user roles (admin, regular, unauthenticated)
5. Enable/disable JavaScript
6. Enable/disable cookies
```

### What to Look For

- Authentication flows (login, register, forgot password)
- Admin panels
- File upload functionality
- Error pages
- API endpoints
- Hidden form fields
- JavaScript files

---

## Spidering

| Type | Description |
|------|-------------|
| Passive | Parse responses from manual browsing |
| Active | Automated link/form following |

### User-Directed Spidering (Recommended)

```
1. Configure Burp Proxy
2. Browse manually → Site Map fills automatically
3. Review Site Map → Visit unvisited URLs manually
4. Repeat until no new content
5. Run active spider (optional, after manual exploration)
```

### Key Distinction

> **Discovered URL ≠ Crawled URL.** A link found in a response is discovered. A request sent to that URL is crawled.

---

## robots.txt & sitemap.xml

| File | Purpose | Security Value |
|------|---------|---------------|
| `robots.txt` | Tell crawlers what NOT to index | May reveal hidden paths |
| `sitemap.xml` | List all pages for indexing | Full URL structure |

### robots.txt Example

```
User-agent: *
Disallow: /admin
Disallow: /backup
Disallow: /config
```

> **robots.txt is NOT a security control.** It may reveal sensitive directories.

---

## Backup Files

| Extension | Content |
|-----------|---------|
| `.bak`, `.old`, `.save` | Backup of source code |
| `.zip`, `.tar.gz`, `.rar` | Archive of files/directories |
| `.sql` | Database dump |
| `.DS_Store` | macOS directory metadata |
| `.git/` | Git repository (full source code) |
| `.env` | Environment variables, secrets |
| `web.config`, `.htaccess` | Server configuration |

### Discovery

```
# Common backup locations
/config.php.bak
/database.sql
/backup.zip
/.git/HEAD
/.env
/wp-config.php.bak
```

---

## Directory Discovery

| Tool | Purpose |
|------|---------|
| Burp Intruder | Brute force directories/files |
| ffuf | Fast web fuzzer |
| dirsearch | Directory discovery |
| Gobuster | Directory/DNS brute force |

### Wordlists

| Wordlist | Source |
|----------|--------|
| SecLists | `Discovery/Web-Content/` |
| common.txt | Default for most tools |
| raft-medium-directories.txt | Medium-sized directory list |
| directory-list-2.3-medium.txt | OWASP |

### Method

```
1. Learn normal vs invalid responses (200 vs 404)
2. Start from discovered directories
3. Use context-aware wordlists
4. Analyze by: status code, response length, response time
5. Enumerate recursively — every new dir is a new target
```

---

## Interesting Extensions

| Extension | Why Interesting |
|-----------|----------------|
| `.php`, `.asp`, `.jsp` | Server-side code |
| `.js`, `.mjs` | Client-side code (APIs, secrets) |
| `.json`, `.xml` | Data files, API responses |
| `.env` | Environment configuration |
| `.log` | Log files |
| `.sql` | Database dumps |
| `.bak`, `.old` | Backup files |
| `.config`, `.conf` | Configuration files |
| `.git`, `.svn` | Version control |

---

## JavaScript Enumeration

> JavaScript files are one of the richest sources of information during recon.

### What to Look For

| Item | Description |
|------|-------------|
| API endpoints | Hardcoded URLs in fetch/XHR calls |
| Parameters | Hidden or undocumented parameters |
| Secrets | API keys, tokens, credentials |
| Internal paths | Development routes, admin panels |
| Third-party services | External APIs, CDNs |
| Function names | Reveal business logic |

### Where to Find JS Files

```
<script src="/static/app.js"></script>
<script src="/assets/bundle.min.js"></script>
```

Also check:
- HTML source for inline scripts
- Source maps (`.js.map`)
- `webpack://` references
- Minified bundles

---

## API Discovery

| Method | Description |
|--------|-------------|
| JavaScript analysis | Find API calls in client-side code |
| Swagger/OpenAPI | `/swagger.json`, `/api-docs` |
| OPTIONS requests | May reveal allowed methods |
| Error messages | May reveal API structure |
| WADL/WSDL | `/api.wadl`, `/service.wsdl` |

### Common API Patterns

```
/api/v1/users
/api/v2/users
/graphql
/rest/api/
/swagger-ui/
/api-docs
```

---

## Technology Fingerprinting

| Source | Information |
|--------|-------------|
| `Server` header | Web server software/version |
| `X-Powered-By` | Framework/language |
| Cookies | Framework (PHPSESSID, JSESSIONID, ASP.NET_SessionId) |
| Headers | CDN, WAF, proxy |
| Error pages | Framework identification |
| HTML source | Generator meta tags, comments |

### Quick Fingerprints

| Identifier | Technology |
|------------|-----------|
| `PHPSESSID` | PHP |
| `JSESSIONID` | Java |
| `ASP.NET_SessionId` | ASP.NET |
| `connect.sid` | Express.js |
| `csrftoken` | Django |
| `laravel_session` | Laravel |

---

## What to Record

| Category | Details |
|----------|---------|
| Entry points | URLs, parameters, headers, cookies |
| Technologies | Framework, language, server, CMS, WAF |
| Endpoints | All discovered API endpoints |
| Parameters | Every parameter name and type |
| Hidden content | Directories, files, backup files |
| JavaScript info | API endpoints, secrets, internal paths |
| Authentication | Login flows, token types, session behavior |
| Access control | Role-based endpoints, authorization boundaries |

---

## Bug Bounty Notes

- [ ] Did you enumerate all subdomains?
- [ ] Did you check robots.txt and sitemap.xml?
- [ ] Did you look for backup files (.bak, .old, .zip)?
- [ ] Did you enumerate directories with wordlists?
- [ ] Did you analyze all JavaScript files for APIs/secrets?
- [ ] Did you check for Swagger/OpenAPI documentation?
- [ ] Did you fingerprint the technology stack?
- [ ] Did you look for source code in .git or .env?
- [ ] Did you test different user roles?
- [ ] Did you discover all API endpoints?

---

## Checklist

```
□ Enumerated subdomains
□ Checked robots.txt and sitemap.xml
□ Searched for backup files (.bak, .old, .zip, .sql)
□ Searched for .git directory and .env files
□ Enumerated directories and files
□ Analyzed JavaScript files for API endpoints
□ Checked for API documentation (Swagger, OpenAPI)
□ Fingerprinted technology stack
□ Completed manual browsing of all features
□ Built comprehensive site map
□ Tested with different user roles
□ Discovered hidden parameters
□ Documented all entry points
```

---

## References

- [SecLists Wordlists](https://github.com/danielmiessler/SecLists)
- [PortSwigger: Recon](https://portswigger.net/web-security)
- [OWASP Recon Cheat Sheet](https://owasp.org/www-project-web-security-testing-guide/latest/2-Reconnaissance_and_Gathering_Information)

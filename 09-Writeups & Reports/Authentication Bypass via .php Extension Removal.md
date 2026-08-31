# Case Study — Authentication Bypass via .php Extension Removal

> **Original write-up:** [Intigriti — Author's write-up](https://...)  
> **Core principle:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (URL normalization mismatch between access-control layer and application router).

---

## TL;DR

Unauthenticated access to **all user videos** on `videos.jaibalayya.de` via URL normalization mismatch: `/videos.php` requires auth, `/videos` does not. Directory listing on `/media/` exposed direct video file paths. Zero credentials, zero payloads.

---

## The Chain

### 0) Scope & Recon
- **Scope:** `*.jaibalayya.de` (wildcard)
- **Method:** Manual VirusTotal enumeration (70+ subdomains)
- **Target:** `videos.jaibalayya.de` → serves single SVG image

> **Foundation:** [[04-Recon/Discovering Hidden Content/Methodology.md]] — manual browsing > automated brute force; [[04-Recon/Manual Browsing.md]]

### 1) Entry Point — SVG Source Path
- Browser: right-click image → "Open image in new tab"
- Discovered: `https://videos.jaibalayya.de/img/x.svg`
- Tested path variation: `/img/y.svg` → **404 with application navigation menu**

> **Foundation:** [[04-Recon/Discovering Hidden Content/Other Resources to Site's content.md]] — images as attack surface clues  
> **Observation:** Custom 404 page leaks application UI (navigation tabs: Edit Video, Thumbnailer, Add Video, How to Use, Videos)

### 2) Target Identification
- Clicked **Videos** tab → redirected to `/videos.php`
- **Authentication required** (login prompt)

> **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Phase 2 - Identify Attack Surface|Phase 2 — Identify Attack Surface]] — collect protected endpoints

### 3) Bypass — Extension Removal
- Hypothesis: Same resource accessible via different URL form
- Tested: `/videos` (removed `.php`)
- **Result: Full access** — all user videos listed with direct media paths (`/media/videoname/videoname.mp4`)

> **Foundation:** [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 4 - Try Alternative Requests|Step 4 — Try Alternative Requests]] → URL Manipulation (extension removal, trailing slash, case, encoding)  
> **Root cause:** Access-control middleware checks `/videos.php` but router normalizes `/videos` → same PHP application, different auth decision

### 4) Impact Expansion — Directory Listing
- From video paths discovered: `/media/`
- **Directory listing enabled** → enumerated all video directories/files (oldest → newest)
- Direct file access: `/media/video1/video1.mp4`, `/media/video2/video2.mp4`, etc.

> **Foundation:** [[04-Recon/Discovering Hidden Content/Methodology.md]] — recursive content discovery; [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access controls|Vertical Access Control]] bypass + [[04-Recon/Discovering Hidden Content/Brute Force.md]] — directory listing as unauthorized file exposure

---

## Key Takeaways

1. **One principle, two findings** — extension removal bypass + directory listing = same class: server/component interpretation mismatch
2. **Protected endpoint ≠ protected resource** — always ask: *"How else can this resource be addressed?"*
3. **Test URL normalization variants systematically:**
   - Extension: `/admin.php` vs `/admin`
   - Trailing slash: `/admin` vs `/admin/`
   - Case: `/Admin` vs `/admin`
   - Encoding: `/admin%2ephp` vs `/admin.php`
   - Matrix params: `/admin;param` vs `/admin`
   - Double path: `/admin/admin` vs `/admin`
4. **Custom error pages leak attack surface** — 404 with navigation = application fingerprint
5. **Impact = scope + chain** — single bypass → all videos → directory listing → all files
6. **Manual > automated** — VirusTotal + browser inspection found what tools missed

---

## Concept Mapping

| Stage | Repo Reference |
|-------|----------------|
| Subdomain enumeration | [[07-CheatSheets/Recon.md#Subdomain Enumeration]] |
| Manual browsing / image analysis | [[04-Recon/Manual Browsing.md]] |
| Custom 404 as info leak | [[04-Recon/Discovering Hidden Content/Other Resources to Site's content.md]] |
| Access control testing methodology | [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md]] |
| URL manipulation variants | [[03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md#Step 4 - Try Alternative Requests]] |
| Directory listing exposure | [[04-Recon/Discovering Hidden Content/Brute Force.md]] |
| Component interpretation mismatch | [[03-Web-Vulnerabilities/temp.md]] |

---

## New Techniques (Gaps to Document)

1. **Custom 404 pages as application discovery vector** — not documented in recon notes
2. **Extension removal as canonicalization bypass** — listed in methodology but no dedicated note with examples
3. **Path traversal via image source paths** — using static asset paths to map application structure

---

## References

- Original write-up (Intigriti private program — link pending)
- Technique credit: URL normalization / canonicalization mismatch class
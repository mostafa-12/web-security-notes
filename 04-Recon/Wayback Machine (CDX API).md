# Wayback Machine & CDX API — Historical Recon

> Recon technique from the case study [[09-Writeups & Reports/API Misconfiguration - PII Leak (100k users)]].

## Concept

The Internet Archive (non-profit) takes **snapshots** of web pages over time. Anything ever public on the internet tends to stay archived **forever** — even after it's deleted, rotated, or hidden on the live site. This makes the archive a recon gold mine:

- Old versions of pages (removed content).
- Secrets that were rotated out of live files (invite codes, API keys, tokens).
- Subdomains, JS bundles, admin paths, backup files that no longer exist live.

> **Key idea:** *Rotation is only surface-level.* Deleting a secret from the live site doesn't delete it from history. "Gone" ≠ gone.

---

## Building Blocks

### 1) Wayback Machine
`https://web.archive.org/` — the main UI. You browse archived copies of a URL like a normal page.

### 2) web.archive.org
The domain that hosts everything. Common URL shapes:

| URL | What it does |
|---|---|
| `https://web.archive.org/web/<timestamp>/<url>` | Opens a specific snapshot (e.g. `20260818000000`) |
| `https://web.archive.org/web/*/<url>` | **Wildcard timestamp** → returns a list of ALL snapshots of that URL across time |
| `https://web.archive.org/web/2/<url>` | Latest snapshot (prefix `2` = any timestamp starting with 2) |

### 3) Wayback CDX API
The **programmatic** interface. Instead of clicking through the UI, you query the archive's index and get machine-readable results. Endpoint:

```
https://web.archive.org/cdx/search/cdx
```

---

## The 2-Step Wayback Workflow

> These are two DIFFERENT techniques serving two different goals — don't mix them up.

### Step A — Snapshot versioning of ONE asset (recover rotated secrets)

```
https://web.archive.org/web/*/go.target.com/55932.js
```

Lists **every historical version** of that single file. Each version can contain **different secrets** (codes rotated out of the live copy). Download each snapshot → extract what changed.

- **Use when:** you found a file that *used to* hold secrets, and want everything it ever contained.
- **No `collapse`** — you want the full history, not a deduped list.

### Step B — Domain-wide URL discovery (find new targets)

```
https://web.archive.org/cdx/search/cdx?url=*.app.target.com&fl=original&collapse=urlkey
```

Returns every **distinct** archived URL under the domain (subdomains/paths ever captured). New old JS files, admin pages, endpoints you never knew existed.

- **Use when:** you want to map what the app looked like across its whole lifetime.
- **`collapse=urlkey` here** — dedupes the same URL repeated across hundreds of capture dates.

---

## CDX API Parameters (the important ones)

```
https://web.archive.org/cdx/search/cdx?url=<pattern>&fl=<fields>&collapse=<key>&from=<yyyy>&to=<yyyy>&filter=<field>:<value>
```

| Param | Meaning | Example |
|---|---|---|
| `url` | The URL pattern to search. `*.domain` = all subdomains; `domain/path*` = all paths | `url=*.app.target.com` |
| `fl` | **F**ield **L**ist — which columns to return (`original`, `timestamp`, `statuscode`, `mimetype`, `digest`...) | `fl=original` |
| `collapse` | Deduplicate results by a key (e.g. `urlkey` = keep one row per unique URL; `timestamp` = one per time bucket) | `collapse=urlkey` |
| `from` / `to` | Date range filter (YYYY or YYYYMMDD) | `from=2020&to=2024` |
| `filter` | Keep only rows matching a field value | `filter=statuscode:200`, `filter=mimetype:application/javascript` |
| `output` | Response format (`json`, `text`, `xml`) | `output=json` |
| `limit` | Max rows | `limit=1000` |

### `collapse=urlkey` — لما نستخدمه وإمتى

The same URL is captured **tens/hundreds of times** across the years:

```
app.target.com/55932.js   ← 2020
app.target.com/55932.js   ← 2021
app.target.com/55932.js   ← 2021
app.target.com/55932.js   ← 2022
... (50+ more)
```

- **Without `collapse`:** 50k rows, mostly the same URLs repeated → noise.
- **With `collapse=urlkey`:** one row per **unique URL** → a clean list of distinct endpoints that ever existed.

> `collapse` removes duplicate **URLs**, not distinct **paths**. The output is still every unique endpoint the app ever had — deduping loses *nothing* you need for URL discovery (content is fetched later, per snapshot, with *no* collapse).

**When to use / not use:**

| Goal | Use collapse? |
|---|---|
| Enumerate distinct URLs (Step B) | ✅ `collapse=urlkey` |
| Recover all versions/secrets of one file (Step A) | ❌ keep the full history |
| Find *when* something appeared / response codes | ❌ you need `fl=timestamp,statuscode` rows |

---

## Combining with `fl` and `filter` — practical queries

```text
# all distinct JS files ever archived under the domain
?url=*.app.target.com&fl=original&collapse=urlkey&filter=mimetype:application/javascript

# URLs that returned 200 (real pages, not 404s)
?url=*.app.target.com&fl=original&collapse=urlkey&filter=statuscode:200

# everything from the early days
?url=*.app.target.com&fl=original&collapse=urlkey&from=2020&to=2023

# JSON output for scripting
?url=*.app.target.com&fl=original,timestamp,statuscode&collapse=urlkey&output=json
```

---

## Automating it (Python)

> `waybackpy` is the friendly wrapper. Raw `requests` also works fine.

```python
import waybackpy

# Step B: distinct URLs under a subdomain
cdx = waybackpy.CDXSnapshot(
    url="*.app.target.com",
    url_key="urlkey",
    collapse="urlkey",
    fl="original",
)
for url in cdx.snapshots():
    print(url)

# Step A: all historical versions of one file
url = "go.target.com/55932.js"
saved = waybackpy.Url(url, user_agent="...")
# then iterate saved... snapshots for each version
```

```bash
# no libraries — plain curl
curl "https://web.archive.org/cdx/search/cdx?url=*.app.target.com&fl=original&collapse=urlkey"
```

---

## Further Study / Other Sources

- **Official:** [CDX API docs (archive.org)](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) — full parameter reference.
- **Tools:**
  - [`waybackpy`](https://github.com/akamhy/waybackpy) — Python wrapper for snapshots + CDX.
  - `waybackurls` — Go CLI: feed it a domain, get all archived URLs (the recon standard, used by most bug bounty toolchains).
  - `gau` (GetAllURLs) — aggregates Wayback + AlienVault OTX + Common Crawl + URLScan in one command.
  - [`gospider`](https://github.com/jaeles-project/gospider) — passive sources + crawling combined.
- **Sister archives:** `web.archive.org` isn't the only one — also check:
  - Common Crawl (`https://index.commoncrawl.org/`) — big web crawls, same kind of URL index API.
  - VirusTotal's URL intelligence, `urlscan.io`, `OTX AlienVault` — all keep historical URL data.
  - Google/Bing cache as a fallback for very recent content.
- **Bug bounty usage:** search GitHub for "waybackurls + gau recon" — the standard passive-recon pipeline is `subdomains → waybackurls/gau → dedupe → filter JS/JSON → grep for secrets & endpoints`.
- **Caution:** this is passive recon on data *already public*. Do not use archived secrets against targets you don't own or aren't authorized to test — that's the same legal boundary as any other recon.

---

## Related Notes

- [[04-Recon/Discovering Hidden Content/Other Resources to Site's content.md|Using Public Information]] — Wayback mentioned as a source; this note is the detailed deep-dive.
- [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]] — the methodology this feeds into.
- [[09-Writeups & Reports/API Misconfiguration - PII Leak (100k users).md|Case study]] — where the technique proved itself (rotated invite codes → 100k PII).
- [[07-CheatSheets/Recon.md|Recon cheat sheet]]
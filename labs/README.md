# Labs — Practice the Writeups Yourself

Each lab recreates one writeup from `09-Writeups & Reports/` as a single realistic-level challenge.
Uniform setup: **Python + Flask**. Install once from the `labs/` folder:

```powershell
cd labs
python -m pip install -r requirements.txt
```

Then run any lab:

```powershell
python labs/lab-01-training-platform-bypass/app.py
# open http://127.0.0.1:8001
```

## Rules
1. Read the lab's `README.md` first (goal + success criteria).
2. Do NOT open `app.py` or `SOLUTION.md` until you capture the flag yourself with Browser/Burp/curl.
3. After solving: read the SOLUTION, compare your approach to the original writeup, then write the takeaway in your notes.

## Labs

| Lab | Recreates | Port | Idea in one line |
|-----|-----------|------|------------------|
| [lab-01-training-platform-bypass](lab-01-training-platform-bypass/) | Training Platform - Login Bypass to Full Admin | 8001 | trailing slash + double path + readOnly `1→0` |
| [lab-02-plan-restriction-bypass](lab-02-plan-restriction-bypass/) | Plan Restriction Bypass ($469) | 8002 | paid feature hidden in UI, open on the API |
| [lab-03-api-pii-leak](lab-03-api-pii-leak/) | API Misconfiguration - PII 100k | 8003 | auth without authz + non-expiring invite codes in JS + archive |
| [lab-04-algolia-exposure](lab-04-algolia-exposure/) | Algolia Key Over-Exposure 154k | 8004 | over-permissioned public key + filters/facets + 2nd index + source map |
| [lab-05-idor-s3-reports](lab-05-idor-s3-reports/) | IDOR + Public S3 Report | 8005 | async job (`postId→jobId`) + public bucket + ListBucket |
| [lab-06-internal-to-admin](lab-06-internal-to-admin/) | Internal User to Admin | 8006 | dual endpoints + unchecked `companyUserRoles` |
| [lab-07-php-extension-bypass](lab-07-php-extension-bypass/) | Auth Bypass via .php Removal | 8007 | `/videos.php` protected, `/videos` open + directory listing |
| [lab-08-jwt-refresh-flaw](lab-08-jwt-refresh-flaw/) | JWT design flaw ($1450) | 8008 | refresh JWT as the session (signature-only, no jti/rotation) |

## Suggested order
```
07 -> 01 -> 02 -> 06 -> 03 -> 05 -> 04 -> 08
(easy URL tricks first, crypto/design hardest last)
```

## Project structure (same pattern in every lab)

```
lab-XX-name/
  app.py         routes only - thin handlers, no business logic here
  config.py      settings (port, flag, keys, tokens)
  store.py       fake database + business logic (lab-08 calls it auth.py)
  static/        JS bundles / assets, as a real app would serve them
  templates/     HTML pages (Jinja2)
  README.md      your briefing (goal + hints)
  SOLUTION.md    sealed until you capture the flag
```

Reading order after solving: `app.py` (what is exposed?) → `store.py`
(where is the missing check? - search for `VULN`) → `config.py`.
Shared dependency for all labs: `requirements.txt` (`flask>=3.0`).

## Why Flask?
- Closer to real apps than raw `http.server`: routing, JSON handling, and cookies work the way production code does.
- One shared `requirements.txt` (`flask>=3.0`) for all 8 labs — install once.
- Each `app.py` stays short and readable so you can review the root cause and the fix after solving.

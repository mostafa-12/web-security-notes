# Lab-07 — Auth Bypass via .php Extension Removal

**Recreates:** `Authentication Bypass via .php Extension Removal.md`
**Run:** `python app.py` → `http://127.0.0.1:8007`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.

## Scenario
A video site. `/videos.php` requires login, but the router and the auth middleware interpret the same URL differently. Plus an open `/media/` directory listing and a custom 404 page that leaks the site map.

## Your goal (zero credentials)
Open all user videos + capture the flag + list every file.

## Starting points
- Open `/`, right-click the image → open image in new tab (`/img/x.svg`).
- Try `/img/y.svg` — read what the 404 says.

## Success criteria
- The videos page + `FLAG{...}` with no cookies, and `Index of /media/`.

## Hints
<details><summary>Hint 1</summary>The 404 page has a nav menu — it names the protected page.</details>
<details><summary>Hint 2</summary>Protected endpoint != protected resource. Try the same name without .php.</details>
<details><summary>Hint 3</summary>From the mp4 paths, infer the folder name and open it directly.</details>

Solution in `SOLUTION.md`.

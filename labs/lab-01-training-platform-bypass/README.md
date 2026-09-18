# Lab-01 — Training Platform: Login Bypass to Full Admin

**Recreates:** `09-Writeups & Reports/Training Platform - Login Bypass to Full Admin.md`
**Run:** `python app.py`, then open `http://127.0.0.1:8001`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**Tools:** Browser + Burp (Repeater/Proxy) only. No credentials.

## Scenario
An internal training platform. The login page discloses ASP.NET. A forgotten, open SSRS instance leaks a `Content_Usage` report (a site map), and Backbone.js files reveal where the admin panel lives.

## Your goal
Get unauthenticated **write access** on user profiles and extract the flag.

Three stages, like the original writeup:
1. From `/ReportServer`, find the most-visited pages.
2. From a JS file, predict the admin path (`views/users/index.js`).
3. Open the admin search page, then the edit-profile page, then actually write to it.

## Starting points (not cheating)
- `GET /` — the login page
- `GET /ReportServer`
- The `X-Powered-By` header discloses the technology

## Success criteria
- `GET` the admin search page with no credentials → `200`
- `POST` a username change with no credentials → response contains `FLAG{...}`

## Off limits
- Do not read `app.py` before trying (it IS the answer). Try with Burp/Browser first.
- No brute-forcing. Every path is hinted inside the lab itself.

## Gradual hints
<details><summary>Hint 1</summary>Open /ReportServer, then Content_Usage. It is your wordlist.</details>
<details><summary>Hint 2</summary>courses/index.js says view names mirror .aspx names. Guess the users path.</details>
<details><summary>Hint 3</summary>Try a trailing slash on the blocked path. And try doubling the path — read what the error says.</details>
<details><summary>Hint 4</summary>The edit page returns readOnly:1. That check lives in JS only. Intercept it, flip it to 0, then POST.</details>

Full solution in `SOLUTION.md` — open it only after capturing the flag.

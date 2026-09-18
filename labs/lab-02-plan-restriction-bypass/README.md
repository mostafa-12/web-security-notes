# Lab-02 — Plan Restriction Bypass (Free → Paid)

**Recreates:** `Plan Restriction Bypass - Free Tier to Paid Features.md` (Sentry/Splunk — $469)
**Run:** `python app.py` → `http://127.0.0.1:8002`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**Accounts:** switch users with the `X-User: free` or `X-User: paid` header (no password in this lab).

## Scenario
Data Forwarding is a paid feature. The dashboard hides it from the free plan. But the settings page and the REST API still exist on the server.

## Your goal
From a **free** account, enable forwarding and find the flag in the response.

## Starting points
- `GET /` with `X-User: free` — see what is shown vs hidden (View Source).
- `GET /static/app.js` — search for `plugins/splunk`.

## Success criteria
- A successful `PUT` from the free account returns `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>UI hiding is not enforcement. Take the path convention from the JS bundle.</details>
<details><summary>Hint 2</summary>Try deep-linking the settings page directly as the free user.</details>
<details><summary>Hint 3</summary>The API is the real boundary: PUT /api/0/projects/org-1/proj-123/plugins/splunk/ with JSON containing instance/index/source/token.</details>

Solution in `SOLUTION.md`.

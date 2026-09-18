# Lab-03 — API Misconfiguration → PII Leak (100k users simulation)

**Recreates:** `API Misconfiguration - PII Leak (100k users).md`
**Run:** `python app.py` → `http://127.0.0.1:8003`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**Login:** any `X-Session: attacker` header counts as logged in.

## Scenario
The participants endpoint requires login but never verifies you are a member of that board. Invite codes never expire and are sitting in a forgotten JS file, plus an archived copy holding old codes that were removed from live but still work.

## Your goal
As `attacker` (member of no board), pull PII for a board you don't own and reach the flag.

## Starting points
- `GET /static/55932.js` — the current code
- `GET /archive/55932.js` — the Wayback copy (rotated codes)

## Success criteria
- `GET /manager/api/brainstorms/<uuid>/participants` returns PII + `FLAG{...}` without membership.

## Hints
<details><summary>Hint 1</summary>A code = membership. POST /join/CODE joins the board.</details>
<details><summary>Hint 2</summary>Try pulling participants for a board you never joined. The endpoint only checks login.</details>
<details><summary>Hint 3</summary>The old code in the archive is still valid because invites never expire.</details>

Solution in `SOLUTION.md`.

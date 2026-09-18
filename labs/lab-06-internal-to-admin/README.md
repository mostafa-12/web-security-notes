# Lab-06 — From Internal User to Admin

**Recreates:** `From Internal User to Admin - Broken Access Control in SaaS.md`
**Run:** `python app.py` → `http://127.0.0.1:8006`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**Tokens:** `admin-token` (admin) and `internal-token` (low-priv internal user) via `Authorization: Bearer`.

## Scenario
The same feature (inviting a user) has dual endpoints: one for the low-priv user with no roles parameter, one for admins with `companyUserRoles[]`. The UI hides the role dropdown from the weak user, but the backend accepts the parameter from anyone logged in.

## Your goal
As the Internal User, create an account with `manager` or `administrator` privileges and capture the flag.

## Starting points
- Capture the admin request (`POST /api/v1/contacts`) and the weak-user request (`POST /api/v1/companyjoinrequests`) and diff the parameters.
- Your own CSRF token is readable from your own session — it is not an obstacle.

## Success criteria
- `201` from `/contacts` with the internal token + elevated roles + `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>Diff the payloads: what extra field does the admin request carry?</details>
<details><summary>Hint 2</summary>Replay the full admin request but with the low-priv token.</details>

Solution in `SOLUTION.md`.

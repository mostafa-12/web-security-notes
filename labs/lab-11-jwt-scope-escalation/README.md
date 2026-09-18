# Lab-11 — Unauthorized Role Management (over-privileged JWT)

**Recreates:** row `Unauthorized Role Management` in `09-Writeups & Reports/Reports Summary Table.md`
([original write-up](https://medium.com/@bassemwanies2002/broken-access-control-to-gain-unauthorized-role-management-in-a-public-program-6925f83d0dc4))
**Run:** `python app.py` → `http://127.0.0.1:8011`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.

## Scenario
Your Backoffice Editor UI says "Roles & permissions: disabled". The check DOES exist server-side — it reads JWT claims. The bug is in token issuance: your low-privilege token carries `dp.entitlements.plans.read/write`, and the backend trusts those scopes on the roles endpoint.

## Your goal
As the Editor, create a role via the hidden endpoint and capture the flag.

## Starting points
- `POST /login {"user":"editor"}` → JWT. Decode the middle segment (it is just base64url JSON).
- Ask: which scopes does a "Backoffice Editor" hold, and which endpoint consumes them?

## Success criteria
- `201` from `POST /development/entitlements/roles` with the Editor token + `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>The vulnerability is not a missing check - it is an over-granted token. Read YOUR token first.</details>
<details><summary>Hint 2</summary>A scope named "plans" gating "roles" is a namespace smell: one scope, two features.</details>

Solution in `SOLUTION.md`.

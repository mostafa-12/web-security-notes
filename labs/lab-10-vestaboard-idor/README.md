# Lab-10 — Vestaboard IDOR ×3 (identifiers ≠ authorization)

**Recreates:** row `Vestaboard` in `09-Writeups & Reports/Reports Summary Table.md`
([original research](https://rhinosecuritylabs.com/research/vestaboard-vulnerabilities/))
**Run:** `python app.py` → `http://127.0.0.1:8010`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**You are:** `u-bob` — `Authorization: Bearer bob-token` (admin of `board-1001` only).

## Scenario
The platform treats knowing an identifier as proof of access: board IDs open simulators, user IDs drive GraphQL mutations, and the role name comes straight from your request. Nothing is correlated back to your JWT.

## Your goals (three flags... two flags, three techniques)
1. **Unauthenticated read:** fetch a board you were never given, with NO token at all, from `/simulator/<board-id>`.
2. **Cross-user rename:** via GraphQL `updateUser(id:, name:)`, rename a user who isn't you.
3. **Admin → Owner:** your UI only offers `member` in the role dropdown — tamper `role:"owner"` in `updateMemberRole`, then open the owner-only billing page.

## Starting points
- `GET /simulator/board-1001` works with zero headers. Board IDs are sequential.
- `GET /board/board-1001/members` (as bob) shows the UI-limited `assignable_roles`.
- GraphQL takes `{"query":"..."}` — e.g. `mutation { updateUser(id:"u-bob", name:"Bobby") }`.

## Success criteria
- `FLAG{...}` in a stranger's board history (no auth header sent).
- A rename response where `by` != `renamed`.
- `GET /board/board-1001/billing` → `200` as bob + `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>Unguessable IDs stop enumeration, not authorization - and here the IDs are sequential anyway. Try the neighbors.</details>
<details><summary>Hint 2</summary>Swap the id argument to someone else's. The server never asks "is this you?"</details>
<details><summary>Hint 3</summary>UI-limited options are not server-enforced. Send the role value the dropdown would never offer.</details>

Solution in `SOLUTION.md`.

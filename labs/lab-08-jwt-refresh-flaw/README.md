# Lab-08 — JWT Refresh Design Flaw (stateless = takeover)

**Recreates:** `jwt-design-flaw-scenario.md`
**Run:** `python app.py` → `http://127.0.0.1:8008`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.

## Scenario
The backend treats the refresh JWT as the session itself: signature + expiry only. No `jti`, no session store, no rotation, no device binding. Any stolen token = full access until it expires (6 days).

## Your goal
1. **Prove the single source of truth:** log in, delete every cookie except `__Host-refreshToken`, and show you are still authenticated.
2. **Takeover:** steal the victim's token (via `/leak-demo`, which simulates XSS/logs) and replay it as the attacker to get the flag.

## Starting points
- `POST /login` with `{"user":"victim"}`
- `GET /leak-demo` — the simulated leak

## Success criteria
- `GET /api/refresh` with only the victim's token → returns `victim_data.flag`.
- `GET /api/protected` with the access token → `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>The refresh endpoint asks for no session — just the cookie.</details>
<details><summary>Hint 2</summary>The token is a real JWT (HMAC-SHA256). Decode the payload on jwt.io and see what is missing (jti? iss? aud?).</details>

Solution in `SOLUTION.md`.

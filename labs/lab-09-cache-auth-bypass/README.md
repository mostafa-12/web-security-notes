# Lab-09 — Authorization Bypass via Cache Misconfiguration

**Recreates:** row `Cache misconfig` in `09-Writeups & Reports/Reports Summary Table.md`
([original write-up](https://rikeshbaniya.medium.com/authorization-bypass-due-to-cache-misconfiguration-fde8b2332d2d))
**Run:** `python app.py` → `http://127.0.0.1:8009`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**You are:** the attacker — `Authorization: Bearer attacker-token` (owner of `shop-999` only).

## Scenario
`GetOrders` responses are micro-cached for 4 seconds to absorb dashboard spikes. The cache key holds the operation + `shop_id` but NOT the auth context. The victim's dashboard auto-refreshes every ~15s, re-priming the cache each time.

## Your goal
Catch the 4-second window: request the VICTIM's `shop-123` orders as the attacker and capture the flag from a cached response.

## Starting points
- `POST /graphql` with `{"operationName":"GetOrders","variables":{"shop_id":"shop-999"}}` — your own shop works (baseline).
- Same query for `shop-123` → `403` on a cache MISS. That is the real check talking.
- The `X-Cache` header (`HIT`/`MISS`) is your oracle — a contradiction between two identical requests is the signal, not a glitch.

## Success criteria
- One `200` response with `X-Cache: HIT` containing another shop's orders + `FLAG{...}`.

## Hints
<details><summary>Hint 1</summary>Same request, two different answers depending on WHEN you send it. Timing is the variable.</details>
<details><summary>Hint 2</summary>Poll in a tight loop for ~30 seconds (1 req/s is plenty) and watch X-Cache.</details>
<details><summary>Hint 3</summary>Autorize-style instant replay beats manual Repeater here: script it, don't click it.</details>

Solution in `SOLUTION.md`.

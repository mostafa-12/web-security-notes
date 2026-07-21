# HTTP Headers CheatSheet

## Table of Contents

- [Overview](#overview)
- [Request Headers](#request-headers)
- [Response Headers](#response-headers)
- [Security Headers](#security-headers)
- [Authentication Headers](#authentication-headers)
- [Caching Headers](#caching-headers)
- [Proxy-Related Headers](#proxy-related-headers)
- [Cookie Headers](#cookie-headers)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Headers control caching, authentication, security policies, and content handling. Manipulating headers is one of the most common attack vectors in web security.

---

## Request Headers

| Header | Purpose | Testing Value |
|--------|---------|---------------|
| `Host` | Target hostname | Host header injection, password reset poisoning |
| `User-Agent` | Client identity | WAF bypass, fingerprinting |
| `Referer` | Previous page | Referer-based access control bypass |
| `Origin` | Request origin | CORS testing |
| `Accept` | Accepted response types | Content-Type switching |
| `Content-Type` | Body format | JSON/form-data/XML switching |
| `Authorization` | Auth credentials | Token manipulation |
| `Cookie` | Session cookies | Cookie tampering |
| `X-Forwarded-For` | Client IP (via proxy) | IP-based access control bypass |
| `X-Forwarded-Host` | Original Host (via proxy) | Host header injection |
| `X-Original-URL` | Original URL (via proxy) | Path traversal, 403 bypass |
| `X-Rewrite-URL` | Original URL (via proxy) | Path traversal, 403 bypass |
| `If-None-Match` | ETag for caching | Conditional request testing |
| `If-Modified-Since` | Cache validation | Conditional request testing |

---

## Response Headers

| Header | Purpose |
|--------|---------|
| `Content-Type` | Response body format |
| `Content-Length` | Body size |
| `Location` | Redirect target |
| `Set-Cookie` | Issues cookies |
| `Server` | Server software (may leak version) |
| `X-Powered-By` | Framework/language info |
| `WWW-Authenticate` | Auth challenge |
| `ETag` | Resource version for caching |
| `Cache-Control` | Caching policy |
| `Allow` | Supported HTTP methods |

---

## Security Headers

| Header | Purpose | Value |
|--------|---------|-------|
| `Strict-Transport-Security` | Force HTTPS | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Restrict resource sources | Complex directive list |
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `X-Frame-Options` | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| `Referrer-Policy` | Control Referer leakage | `no-referrer` |
| `Permissions-Policy` | Restrict browser features | Feature restrictions |
| `X-XSS-Protection` | Legacy XSS filter | `1; mode=block` (deprecated) |

### Missing Security Headers = Easy Findings

| Missing Header | Risk |
|---------------|------|
| `Strict-Transport-Security` | HTTP downgrade attacks |
| `Content-Security-Policy` | XSS, data exfiltration |
| `X-Content-Type-Options` | MIME type confusion |
| `X-Frame-Options` | Clickjacking |

---

## Authentication Headers

| Header | Format |
|--------|--------|
| `Authorization: Basic` | `Basic base64(user:pass)` |
| `Authorization: Bearer` | `Bearer <JWT>` |
| `WWW-Authenticate` | Challenge from server (401 response) |

---

## Caching Headers

| Header | Value | Meaning |
|--------|-------|---------|
| `Cache-Control` | `no-store` | Never cache |
| | `no-cache` | Cache but revalidate |
| | `max-age=3600` | Cache for 3600 seconds |
| | `private` | Only browser can cache |
| | `public` | Any proxy can cache |
| `Pragma` | `no-cache` | HTTP/1.0 backward compatibility |
| `Expires` | `0` or past date | Cache expired |

> **Security Impact:** Sensitive pages should use `no-store, private`. Caching of auth pages may leak data to shared computers.

---

## Proxy-Related Headers

| Header | Purpose |
|--------|---------|
| `X-Forwarded-For` | Client IP (may contain multiple IPs) |
| `X-Forwarded-Proto` | Original protocol (http/https) |
| `X-Forwarded-Host` | Original Host header |
| `Via` | Indicates proxy involvement |

```
X-Forwarded-For: client, proxy1, proxy2
```

> The leftmost IP is the original client. Traversal: each proxy appends to the right.

---

## Cookie Headers

| Direction | Header | Example |
|-----------|--------|---------|
| Server → Browser | `Set-Cookie` | `Set-Cookie: session=abc; HttpOnly; Secure` |
| Browser → Server | `Cookie` | `Cookie: session=abc; token=xyz` |

---

## Bug Bounty Notes

- [ ] Is `Server` or `X-Powered-By` leaking framework/version info?
- [ ] Can `X-Forwarded-For` bypass IP-based restrictions?
- [ ] Can `X-Original-URL` or `X-Rewrite-URL` bypass path-based 403?
- [ ] Is the `Referer` header being validated for access control?
- [ ] Does removing the `Origin` header change CORS behavior?
- [ ] Can `Host` header be manipulated (password reset poisoning, SSRF)?
- [ ] Are sensitive pages cached (`Cache-Control` missing or misconfigured)?
- [ ] Can you upgrade from HTTP to HTTPS by manipulating `X-Forwarded-Proto`?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Trusting `X-Forwarded-For` for IP restrictions | Client-controlled header |
| Ignoring missing security headers | Each missing header = potential finding |
| Not testing header injection | CRLF injection via headers |
| Assuming CORS is configured correctly | Always verify `Access-Control-Allow-Origin` |

---

## Checklist

```
□ Checked for Server/X-Powered-By information leakage
□ Tested X-Forwarded-For for IP-based bypass
□ Tested X-Original-URL / X-Rewrite-URL for 403 bypass
□ Verified security headers (HSTS, CSP, X-Frame-Options, etc.)
□ Checked Cache-Control on sensitive pages
□ Tested Host header injection
□ Verified CORS configuration
□ Tested Referer-based access control
□ Checked Set-Cookie attributes (HttpOnly, Secure, SameSite)
```

---

## References

- [MDN Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [PortSwigger Headers](https://portswigger.net/web-security/headers)
- [OWASP HTTP Headers](https://owasp.org/www-project-secure-headers/)

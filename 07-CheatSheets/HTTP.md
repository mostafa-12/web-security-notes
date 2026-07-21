# HTTP CheatSheet

## Table of Contents

- [Overview](#overview)
- [Request Structure](#request-structure)
- [Response Structure](#response-structure)
- [HTTP Methods](#http-methods)
- [GET vs POST](#get-vs-post)
- [PUT vs PATCH](#put-vs-patch)
- [Idempotent & Safe Methods](#idempotent--safe-methods)
- [Content Types](#content-types)
- [Cookies](#cookies)
- [HTTPS](#https)
- [REST](#rest)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> HTTP is a stateless, message-based protocol — every request is independent and carries all the information the server needs.

---

## Request Structure

```http
GET /path/page?id=123 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Cookie: session=abc123
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json

{"key": "value"}
```

| Component | Purpose |
|-----------|---------|
| Method | Action (GET, POST, etc.) |
| Path | Resource location |
| Query String | Parameters (`?key=value&key2=value2`) |
| Version | HTTP version (1.1, 2, 3) |
| Headers | Metadata |
| Body | Data payload (POST/PUT) |

---

## Response Structure

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=abc123; HttpOnly; Secure
Location: https://example.com/dashboard
Content-Length: 1024

<!DOCTYPE html>...
```

---

## HTTP Methods

| Method | Purpose | Body | Safe | Idempotent |
|--------|---------|------|------|------------|
| GET | Retrieve resource | No | Yes | Yes |
| HEAD | Like GET, no body | No | Yes | Yes |
| POST | Create / submit data | Yes | No | No |
| PUT | Replace resource entirely | Yes | No | Yes |
| PATCH | Partially update resource | Yes | No | No |
| DELETE | Remove resource | No | No | Yes |
| OPTIONS | Describe communication options | No | Yes | Yes |
| TRACE | Loop-back test (debug) | No | Yes | Yes |
| CONNECT | Establish TCP tunnel | No | No | No |

> **Safe** = does not modify server state. **Idempotent** = same request repeated has the same effect as once.

---

## GET vs POST

| Feature | GET | POST |
|---------|-----|------|
| Data location | URL query string | Request body |
| Bookmarked | Yes | No |
| Cached | Yes | Rarely |
| Length limit | URL length (~2048 chars) | No strict limit |
| Sensitive data | Never use for passwords | Preferred |
| Browser back/refresh | Harmless | May re-submit |

---

## PUT vs PATCH

| | PUT | PATCH |
|--|-----|-------|
| Scope | Replace entire resource | Modify specific fields |
| Body | Full representation | Partial update |
| Idempotent | Yes | Not necessarily |

```http
PUT /api/users/123 HTTP/1.1
Content-Type: application/json

{"name": "Ahmed", "email": "a@test.com", "role": "user"}
```

```http
PATCH /api/users/123 HTTP/1.1
Content-Type: application/json

{"role": "admin"}
```

---

## Content Types

| Content-Type | Usage |
|-------------|-------|
| `text/html` | HTML pages |
| `application/json` | JSON APIs |
| `application/x-www-form-urlencoded` | Default form submission |
| `multipart/form-data` | File uploads |
| `text/plain` | Plain text |
| `application/xml` | XML data |
| `application/javascript` | JavaScript files |

### Form Submission Comparison

```
# application/x-www-form-urlencoded
username=ahmed&password=1234

# multipart/form-data (used for file uploads)
------boundary
Content-Disposition: form-data; name="file"; filename="image.jpg"
<binary data>
------boundary--
```

---

## Cookies

| Attribute | Purpose |
|-----------|---------|
| `Domain` | Which domains receive the cookie |
| `Path` | URL path scope |
| `Expires` | Absolute expiry date |
| `Max-Age` | Relative expiry (seconds) |
| `Secure` | HTTPS only |
| `HttpOnly` | No JavaScript access |
| `SameSite` | CSRF protection (Strict / Lax / None) |

### Cookie Prefixes

| Prefix | Protection |
|--------|------------|
| `__Secure-` | Must be HTTPS + Secure |
| `__Host-` | Must be HTTPS + Secure + Path=/ + No Domain |

---

## HTTPS

- HTTP + TLS encryption
- Confidentiality + Integrity
- HTTP semantics unchanged — only transport encrypted
- SSL is deprecated; TLS is current

---

## REST

| Pattern | Example |
|---------|---------|
| Collection | `GET /users` |
| Specific resource | `GET /users/123` |
| Nested resource | `GET /users/123/orders` |
| Action (RPC-style) | `POST /users/123/activate` |

> REST identifies resources by URL. Parameters in path = resource identifier. Parameters in query = filtering/sorting.

---

## Bug Bounty Notes

- [ ] Can GET parameters be manipulated to access other users' data?
- [ ] Is there a hidden PUT/DELETE/PATCH method enabled?
- [ ] Does POST to an authenticated endpoint work without a session?
- [ ] Can JSON body be used instead of form data (content-type switch)?
- [ ] Are there any rate limits on POST requests?
- [ ] Can query strings be tampered with (IDOR)?
- [ ] Does the API accept XML input (XXE potential)?
- [ ] Are there any undocumented endpoints (OPTIONS)?
- [ ] Can the Host header be poisoned?
- [ ] Does the server follow redirects to external domains (open redirect)?

---

## Common Mistakes

| Mistake | Why It's Wrong |
|---------|---------------|
| Testing only GET requests | Hidden methods may have weaker controls |
| Trusting client-side validation | Trivially bypassed with Burp/curl |
| Ignoring OPTIONS responses | May reveal hidden endpoints |
| Not checking Content-Type switches | JSON vs form-data may bypass validation |
| Assuming REST = security | URL structure does not imply access control |

---

## Checklist

```
□ Tested all HTTP methods (OPTIONS, PUT, DELETE, PATCH)
□ Checked for Host header injection
□ Tested Content-Type switching (JSON ↔ form-data ↔ XML)
□ Verified session is required for sensitive endpoints
□ Checked for rate limiting on login/action endpoints
□ Tested parameter pollution
□ Checked for open redirects via query parameters
□ Verified CORS policy (Access-Control-Allow-Origin)
□ Looked for hidden API endpoints in JavaScript
```

---

## References

- [MDN HTTP Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [PortSwigger HTTP](https://portswigger.net/web-security/http)

# HTTP Status Codes CheatSheet

## Table of Contents

- [Overview](#overview)
- [1xx — Informational](#1xx--informational)
- [2xx — Success](#2xx--success)
- [3xx — Redirection](#3xx--redirection)
- [4xx — Client Error](#4xx--client-error)
- [5xx — Server Error](#5xx--server-error)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Status codes tell you what happened to your request. During testing, anomalies in status codes reveal hidden content, access control issues, and server behavior.

---

## 1xx — Informational

| Code | Name                | Meaning                                                                                                                         |
| ---- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 100  | Continue            | Server accepted request headers; continue sending body, client received part of body success and ask server to send other parts |
| 101  | Switching Protocols | Server switching to WebSocket or upgrade protocol                                                                               |

> Rarely seen in manual testing. Usually handled automatically by browsers.

---

## 2xx — Success

| Code | Name       | Meaning                                                                                   |
| ---- | ---------- | ----------------------------------------------------------------------------------------- |
| 200  | OK         | Standard success                                                                          |
| 201  | Created    | Resource created (POST/PUT)                                                               |
| 202  | Accepted   | Request accepted but not yet processed (mission in progress like 101 but for server-side) |
| 204  | No Content | Success with no response body (DELETE)                                                    |

---

## 3xx — Redirection

| Code | Name               | Meaning                    | Follow? |
| ---- | ------------------ | -------------------------- | ------- |
| 301  | Moved Permanently  | Resource permanently moved | Yes     |
| 302  | Found              | Temporary redirect         | Yes     |
| 303  | See Other          | Redirect with GET          | Yes     |
| 304  | Not Modified       | Use cached version         | N/A     |
| 307  | Temporary Redirect | Preserve method            | Yes     |
| 308  | Permanent Redirect | Preserve method            | Yes     |

> **Security Note:** 302 redirects on login can leak the Referer header. Check if the redirect target is validated (Open Redirect).

---

## 4xx — Client Error

| Code | Name | Meaning | Testing Relevance |
|------|------|---------|-------------------|
| 400 | Bad Request | Malformed syntax | May reveal input validation |
| 401 | Unauthorized | **Authentication required** | Name is misleading — means "not authenticated" |
| 403 | Forbidden | Authenticated but **not authorized** | Access control issue if you expected 200 |
| 404 | Not Found | Resource does not exist | Hidden pages may return 200 instead |
| 405 | Method Not Allowed | HTTP method not permitted | May reveal allowed methods in Allow header |
| 408 | Request Timeout | Server timed out | May indicate rate limiting |
| 413 | Payload Too Large | Body too big | Test upload limits |
| 414 | URI Too Long | URL too long | Test parameter limits |
| 415 | Unsupported Media Type | Wrong Content-Type | Content-Type switching test |
| 429 | Too Many Requests | Rate limited | Important for brute force testing |

### 401 vs 403 — The Confusing Ones

| Response | Actual Meaning |
|----------|---------------|
| 401 Unauthorized | "I don't know who you are — log in first" |
| 403 Forbidden | "I know who you are, but you can't do this" |

> **Common mistake:** Thinking 401 means "unauthorized access" — it actually means "unauthenticated."

---

## 5xx — Server Error

| Code | Name | Meaning |
|------|------|---------|
| 500 | Internal Server Error | Unhandled exception — may reveal stack traces |
| 502 | Bad Gateway | Upstream server issue |
| 503 | Service Unavailable | Server overloaded or down for maintenance |
| 504 | Gateway Timeout | Upstream server too slow |

> **500 errors are gold during testing** — they may reveal SQL errors, path information, framework details, or debug output.

---

## Bug Bounty Notes

- [ ] Does a nonexistent page return 200 (custom 404 page)?
- [ ] Do 403 responses change when modifying headers (X-Forwarded-For, etc.)?
- [ ] Can you bypass 403 by changing the HTTP method?
- [ ] Does 500 reveal stack traces or debug information?
- [ ] Is rate limiting returning 429 or 403?
- [ ] Does 302 on login include sensitive data in the redirect URL?
- [ ] Can you force a 500 by sending malformed input (DoS testing)?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Assuming 200 = access granted | Custom 404 pages often return 200 |
| Ignoring 403 | Bypassing 403 = finding access control bugs |
| Ignoring 500 | 500 may leak internals |
| Not checking Allow header on 405 | May reveal hidden methods |

---

## Checklist

- [ ] Tested nonexistent paths — do they return 200 or 404?
- [ ] Checked 403 responses with different methods (GET → POST → PUT)
- [ ] Checked 403 responses with header manipulation (X-Forwarded-For, X-Original-URL)
- [ ] Monitored for 500 errors during input testing
- [ ] Checked for stack traces or debug output in 500 responses
- [ ] Verified rate limit behavior (429 vs 403)
- [ ] Checked Allow header on 405 responses
- [ ] Verified redirect destinations (Open Redirect)


---

## References

- [MDN Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [PortSwigger: HTTP Status Codes](https://portswigger.net/web-security/http)

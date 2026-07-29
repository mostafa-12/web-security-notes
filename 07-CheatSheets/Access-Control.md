# Access Control CheatSheet

## Table of Contents

- [Overview](#overview)
- [Types of Access Control](#types-of-access-control)
- [Vertical Privilege Escalation](#vertical-privilege-escalation)
- [Horizontal Privilege Escalation](#horizontal-privilege-escalation)
- [Forced Browsing](#forced-browsing)
- [Context-Dependent Access Control](#context-dependent-access-control)
- [Common Authorization Flaws](#common-authorization-flaws)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Access control enforces what an authenticated user is allowed to do. Flaws let users access data or perform actions beyond their privileges.

---

## Types of Access Control

| Type | Description | Example |
|------|-------------|---------|
| Vertical | Different privilege levels | User → Admin |
| Horizontal | Same privilege level, different resources | User A accessing User B's data |
| Context-dependent | Access depends on application state | Accessing checkout without completing cart |

---

## Vertical Privilege Escalation

> Low-privileged user accesses admin functionality.

### Common Vectors

| Vector | Description |
|--------|-------------|
| Hidden admin endpoints | `/admin`, `/admin-panel`, `/dashboard` |
| Unprotected admin functions | Admin API without auth checks |
| Parameter manipulation | `role=admin`, `isAdmin=true` |
| HTTP method switching | POST → PUT on admin endpoints |
| Forced browsing | Directly accessing admin URLs |

### Test

```
1. Login as normal user
2. Find admin endpoints (recon, JavaScript, robots.txt)
3. Access admin functionality directly
4. Try changing role/permission parameters
5. Try switching HTTP methods
```

---

## Horizontal Privilege Escalation

> User A accesses User B's data or resources.

### Common Vectors

| Vector | Description |
|--------|-------------|
| Sequential IDs | Predictable resource identifiers |
| Parameter tampering | `user_id=123` → `user_id=124` |
| Referer/Origin manipulation | Modifying request origin |

### Test

```
1. Login as User A
2. Access User A's resources
3. Change the user identifier to User B's
4. Check if User B's data is returned
```

---

## Forced Browsing

> Accessing pages directly without going through the normal application flow.

```
# Normal flow: Login → Dashboard → Settings
# Forced browsing: Directly access /settings without login
```

### Test

```
1. Log out of the application
2. Try accessing internal pages directly
3. Check if authentication is enforced on every page
4. Test with different user roles
```

---

## Context-Dependent Access Control

> Access depends on the application's state or workflow.

```
# Example: Checkout
# Must complete: Cart → Shipping → Payment → Confirmation
# Can you skip directly to /confirmation?
```

---

## Common Authorization Flaws

| Flaw | Description |
|------|-------------|
| Missing function-level access control | Admin endpoint accessible to all users |
| Forced browsing | Direct URL access bypasses checks |
| Parameter manipulation | Changing `admin=false` to `admin=true` |
| HTTP method bypass | Access control on GET but not POST |
| Path traversal bypass | `/admin` blocked, `/admin/` works |
| Case sensitivity bypass | `/Admin` vs `/admin` |
| Header-based bypass | `X-Original-URL` or `X-Rewrite-URL` |

---

## Bug Bounty Notes

- [ ] Can you access admin endpoints as a normal user?
- [ ] Can you access another user's data by changing user IDs?
- [ ] Can you bypass 403 by changing HTTP method?
- [ ] Can you bypass path-based access control with `X-Original-URL`?
- [ ] Can you skip workflow steps (forced browsing)?
- [ ] Does the API verify authorization on every request?
- [ ] Are there any endpoints that don't check authentication at all?
- [ ] Does the application leak data in error messages when access is denied?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Testing only authenticated endpoints | Unauthenticated endpoints may exist |
| Only testing GET | POST/PUT/DELETE may have weaker controls |
| Trusting client-side role | Server must verify on every request |
| Assuming URL = authorization | URL visibility != access control |

---

## Checklist

```
□ Tested vertical privilege escalation (user → admin)
□ Tested horizontal privilege escalation (user A → user B)
□ Tested forced browsing on authenticated pages
□ Tested HTTP method switching on access-controlled endpoints
□ Tested path-based 403 bypass (X-Original-URL, case sensitivity)
□ Verified authorization on every API endpoint
□ Checked for missing function-level access control
□ Checked error messages for information leakage
```

---

## References

- [PortSwigger: Access Control](https://portswigger.net/web-security/access-control)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

# Case Study — From Internal User to Admin: Exploiting Broken Access Control in SaaS Platforms

> **Original write-up:** [Medium — Mohamed Badawy](https://medium.com/@mobadawyx4/from-internal-user-to-admin-exploiting-broken-access-control-in-saas-platforms-c1a2e36489a4)
> **Target:** Anonymous SaaS platform (multi-tenant)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *UI hides role selector* vs *backend accepts role parameter without authorization check*).

---

## TL;DR

An **Internal User** (low-privilege role) escalates to **Manager/Administrator** by calling the administrative invitation endpoint `/api/v1/contacts` directly with their own session token. The UI hides the role selector for Internal Users, but the backend processes the `companyUserRoles` parameter without verifying the requester can assign those roles. Result: any Internal User can invite new accounts with elevated privileges. Report closed as **duplicate**.

---

## The Chain (foundation → application)

### 1) The false assumption to attack
The developer enforced the authorization boundary **only in the UI**:
- Administrator invitation dialog → shows role dropdown (`user`, `manager`, `administrator`)
- Internal User invitation dialog → **no role dropdown**, only email field

**Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] + [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md#Never Trust Client-Controlled Data|Never Trust Client-Controlled Data]] — hiding a control ≠ enforcing a restriction. The UI is client-side; access control must live server-side, per request.

### 2) Mapping the surface — two endpoints, same feature
The application exposes **two distinct endpoints** for inviting users:

| Actor | Endpoint | Purpose | Key Parameter |
|-------|----------|---------|---------------|
| **Internal User** | `POST /api/v1/companyjoinrequests` | Send a "join request" (no role assignment) | `email`, `companyId`, `source` |
| **Administrator** | `POST /api/v1/contacts` | Invite user **with explicit role assignment** | `identifiers[]`, **`companyUserRoles[]`**, `contactType` |

> **Recon insight:** The two endpoints coexist. The Internal User's flow is a *subset* of the Administrator's flow — same feature (invite), different privilege surface. → [[04-Recon/Discovering Hidden Content/Methodology.md|Discovering Hidden Content]] (guided enumeration: find all endpoints that perform the same business function).

### 3) Standard flow analysis

#### A. Low-Privilege Action (Internal User)
```http
POST /api/v1/companyjoinrequests HTTP/1.1
Host: app.example.com
Content-Type: application/json
Authorization: Bearer <INTERNAL_USER_TOKEN>

{
  "identifier": {
    "providerId": "email",
    "providerUserId": "invited_user@example.com"
  },
  "email": "invited_user@example.com",
  "companyId": "12345",
  "source": "company invite dialog"
}
```
> No `roles` parameter. The server creates a pending request or adds the user with a default low-privilege role.

#### B. Administrative Action (Administrator)
```http
POST /api/v1/contacts HTTP/1.1
Host: app.example.com
Content-Type: application/json
Authorization: Bearer <ADMIN_TOKEN>

{
  "identifiers": [
    {
      "providerId": "email",
      "providerUserId": "invited_user@example.com"
    }
  ],
  "companyUserRoles": [
    "user",
    "manager"
  ],
  "contactId": null,
  "contactType": "company"
}
```
> **Critical difference:** `companyUserRoles` array explicitly assigns `manager` (or `administrator`). The backend **accepts this parameter from the request body**.

### 4) Vulnerability execution (bypass)
The `/api/v1/contacts` endpoint validates **authentication** (valid session token) but **fails to enforce authorization** (does the requester have permission to assign `manager`/`administrator` roles?).

An attacker logged in as an **Internal User** crafts the administrative request structure and sends it with their own credentials:

```http
POST /api/v1/contacts HTTP/1.1
Host: app.example.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0
Content-Type: application/json
X-CSRF-Token: <INTERNAL_USER_CSRF>
Cookie: session=<INTERNAL_USER_SESSION>

{
  "identifiers": [
    {
      "providerId": "email",
      "providerUserId": "target_account@example.com"
    }
  ],
  "companyUserRoles": [
    "user",
    "manager"
  ],
  "contactId": null,
  "contactType": "company"
}
```

#### Result
The server returns `200 OK` / `201 Created`. The target account (`target_account@example.com`) is added to the organization with **elevated `manager` privileges**, completely bypassing administrative authorization.

> **CSRF Token note:** The `X-CSRF-Token` is the attacker's own token (read from their browser/cookie/HTML). CSRF tokens protect against *cross-site* request forgery, not *same-session* privilege escalation. The attacker owns the session → they own the CSRF token.

### 5) The missing check
```python
# What the endpoint SHOULD do (pseudocode)
def create_contact(request):
    user = get_user_from_token(request.auth_token)
    
    # MISSING: Authorization check
    if not user.can_assign_role(request.body.companyUserRoles):
        return 403 Forbidden  # "You cannot assign 'manager' role"
    
    # Proceed to create contact with requested roles
    ...
```

The fix is a **single server-side check**: `current_user.max_assignable_role >= requested_role`.

---

## Concept Mapping

- **Vulnerability class:** **Vertical Privilege Escalation / Broken Access Control (BAC)** — low-privilege user performs administrative action (role assignment).
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Missing authorization check on the server — security-through-UI-hiding. The backend trusts the client-supplied `companyUserRoles` parameter without comparing it to the requester's permissions.
  → [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing methodology:** 
  1. Map endpoints per role (Observe)
  2. Diff payloads between privilege levels (Hypothesize)
  3. Replay high-priv payload with low-priv token (Test)
  4. Verify impact (Validate)
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]] + [[02-Web Architecture/Anatomy of a Web Request.md|Trust Boundary & Platform Misconfig]]
- **Multi-tenant context:** Role assignment endpoint is a distinct surface from "change my own role" — it *grants* roles to others. Test both.
- **CSRF token in exploit:** Not a barrier — same-session tokens are readable by the session owner.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Endpoint differentiation as recon** — The same business feature (invite user) exposes **two endpoints** (`/companyjoinrequests` vs `/contacts`) with different privilege requirements. Finding *all* endpoints for a feature reveals the one with missing authz.
2. **`companyUserRoles` / `roles` parameter as privilege escalation vector** — Any parameter that assigns roles/permissions to *another* user must be validated against the requester's **maximum assignable role**, not just their authentication status.
3. **Multi-tenant SaaS: role-granting endpoint ≠ self-role endpoint** — The endpoint that *assigns roles to others* (`/contacts`, `/invitations`, `/memberships`) is a distinct attack surface from the endpoint that *changes your own role* (`/profile`, `/account`). Test both independently.
4. **CSRF token in same-session exploit = not a barrier** — CSRF tokens are per-session secrets readable by the session owner. They prevent *cross-origin* forgery, not *authorized-user* abuse of an over-permissive endpoint.
5. **Duplicate finding ≠ low severity / not reproducible** — "Closed as duplicate" means the pattern is known and recurring in the platform. Test for it anyway; a duplicate in one program may be a valid finding in another.

---

## Key Takeaways

1. **UI hiding ≠ server enforcement** — A missing dropdown in the frontend does not remove the parameter from the backend. Every parameter that affects authorization must be validated server-side.
2. **AuthN ≠ AuthZ, at the parameter level** — The endpoint verified *who you are* (valid token) but not *what you can assign* (`companyUserRoles` vs your role).
3. **Map all endpoints for a feature** — A feature (invite) may have multiple API paths (user-facing, admin-facing, internal). The one with the weakest authz wins.
4. **Role-assignment endpoints are high-value targets** — They directly control privilege distribution. Test: `POST /invitations`, `PUT /memberships/{id}`, `POST /contacts`, `POST /users` with `role`/`roles`/`permissions` parameters.
5. **Multi-tenant RBAC: test cross-role assignment** — Can a `Manager` assign `Admin`? Can an `Internal User` assign `Manager`? The matrix of (requester_role × target_role) is the test space.
6. **Parameter pollution / extra parameters** — If the low-priv endpoint (`/companyjoinrequests`) silently ignores `companyUserRoles`, try adding it. If the high-priv endpoint (`/contacts`) accepts it, the bug is the missing check on *who* can call it.

---

## References

- [From Internal User to Admin: Exploiting Broken Access Control in SaaS Platforms — Mohamed Badawy (Medium)](https://medium.com/@mobadawyx4/from-internal-user-to-admin-exploiting-broken-access-control-in-saas-platforms-c1a2e36489a4)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- Access Control Testing Methodology: [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md]]
- Multi-Step Processes (if async): [[03-Web-Vulnerabilities/Multi-Step Processes.md]]
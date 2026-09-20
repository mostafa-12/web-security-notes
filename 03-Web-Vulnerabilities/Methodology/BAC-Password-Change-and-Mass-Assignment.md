# BAC Hunting: Password-Change Bypass & Mass Assignment

> Source pattern: [[09-Writeups & Reports/The Missing Link - Broken Access Control to Full ATO]] — `Authenticate → Set` on `POST /apiv1` with no link.
> Core rule: [[03-Web-Vulnerabilities/temp.md]] — UI and backend interpret the same flow differently.
> Base loop: [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Observe → Hypothesize → Test]].

---

## 1) The pattern to hunt

Any sensitive action split into **Validate (step 1) then Execute (step 2)**:

```
Change Password:  Authenticate(oldPassword) → Set(password=new)
Change Email:     VerifyOTP / ConfirmPassword → Update(email=new)
Role grant:       Admin picker UI → POST /contacts {roles: [...]}
Profile update:   GET profile (read-only UI) → PUT /profile {name, ...}
```

The bug is always the same: **step 2 executes without proof step 1 happened.**

---

## 2) Step-by-step test procedure

### Step 1 — Map the normal flow (Observe)
1. Do the action once in the UI with Burp Proxy on.
2. Record every request in order (note: same endpoint twice still = 2 steps).
3. For each request, log: method, path, params, what it returns.

### Step 2 — Ask "What is the link?" (Hypothesize)
Inspect what binds step 1 → step 2. One of these must exist:

| Valid link          | Example                                                           |
| ------------------- | ----------------------------------------------------------------- |
| Same-request proof  | `oldPassword` + `newPassword` in ONE body, server verifies hash   |
| Single-use token    | `pwdChangeToken` issued by step 1, consumed by step 2 (short TTL) |
| Server session flag | `session.pendingPwdChange = true` set by step 1, cleared on use   |

If **none** exists → high-confidence candidate. Proceed.

### Step 3 — Isolate step 2 (Test)
1. In Repeater, **drop/delete step 1**.
2. Send step 2 alone with your own session.
3. Variants to try in order:
   - Exact replay of step 2 (no modification)
   - Step 2 with attacker-chosen value (`"password": "Hacking@123"`)
   - Step 2 with victim `id` / `email` swapped (horizontal test: can User A set User B's password?)

### Step 4 — Validate impact (Observe Again)
- `200 OK` alone = write, not takeover. Prove it:
  - Password: fresh incognito login with new password.
  - Email: trigger reset flow to attacker inbox.
  - Role: login as target, screenshot new privileges.

---

## 3) Mass-assignment fuzz on generic update endpoints

Endpoints shaped like `{ "typeName": "User", "entity": { ... } }` / `PUT /profile` / `PATCH /users/{id}` accept whatever keys you send. After any benign update works, fuzz:

```
password, newPassword, oldPassword (omit it on purpose)
email, userName, name
role, roles, companyUserRoles, isAdmin, isStaff
userId, id (swap to victim), groupId, tenantId
```

Rules:
- **One variable at a time** (per [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Isolate Variables]]).
- Start harmless (`firstName: HACKED`), then escalate to `password` / `email` / `role`.
- Always re-GET the object or re-login to confirm persistence.

---

## 4) Quick checklist (copy into Burp notes)

```
□ Did Change Password / Email fire 2+ requests? List them.
□ What links step 1 → step 2? (token / flag / oldPassword / nothing?)
□ Does step 2 alone with fresh session return 200?
□ Does generic update accept "password" / "email" / "role" keys?
□ Can id/userId be swapped to victim (horizontal)?
□ Fresh-login / re-GET proof captured?
□ Threat model noted? (session-only → permanent lockout)
```

---

## 5) Fix reference (for reports)

- **Preferred:** require `oldPassword` + `newPassword` in the SAME request; server verifies hash before write; enforce `requester.id == target.id OR requester.isAdmin`.
- **If two-step required:** step 1 issues short-lived (≤5 min) single-use token bound to `userId`; step 2 must consume it; reject reuse/replay.
- **Generic updates:** whitelist allowed fields per role; strip or reject `password`/`role`/`email` unless the dedicated, authorized flow is used.

---

## Related

- Case study: [[09-Writeups & Reports/The Missing Link - Broken Access Control to Full ATO]]
- Multi-step theory: [[03-Web-Vulnerabilities/Multi-Step Processes.md]] + [[03-Web-Vulnerabilities/Methodology/Multi-step WorkFlow.md]]
- Cheatsheet: [[07-CheatSheets/Access-Control.md]]

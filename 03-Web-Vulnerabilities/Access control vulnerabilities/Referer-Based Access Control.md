
---

# Idea

Some applications use the `Referer` header to determine whether a request is authorized.

Instead of validating the authenticated user's permissions, the application trusts the value of the `Referer` header.

---

# Defect

The `Referer` header is sent by the client.

An attacker can modify or forge it using tools such as Burp Suite.

As a result, authorization decisions based on this header can be bypassed.

---

# Vulnerable Logic

```
Referer == /admin
        ↓
Allow
```

instead of

```
Current User
        ↓
Is Admin?
        ↓
Allow / Deny
```

---

# Example

Legitimate request

```http
POST /admin/deleteUser

Referer: https://site.com/admin
```

Attacker request

```http
POST /admin/deleteUser

Referer: https://site.com/admin
```

Even if the attacker is not an administrator.

---

# Root Cause

The application trusts client-controlled data for authorization.

---

# Impact

- Vertical Privilege Escalation
- Unauthorized Administrative Actions

---


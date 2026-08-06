
---

# Idea

Some sensitive functionality is divided into multiple requests.

Example:

1. Select user
2. Review changes
3. Confirm

---

# Defect

The application checks authorization only in the first steps.

The final request (Confirm) performs the sensitive action **without verifying** that the current user is authorized.

The application trusts the workflow instead of checking permissions on every request.

---

# Lab SOL

1. Login as `administrator`.
2. Promote `carlos`.
3. Capture the **confirmation request** in Burp Repeater.
4. Login as `wiener`.
5. Replace the session cookie with Wiener's session.
6. Change:

```text
username=carlos
```

to

```text
username=wiener
```

7. Send the request.
8. Wiener becomes an administrator.

---

# Root Cause

The application assumes:

```
User reached Confirm page
        ↓
User must be Admin
```

instead of checking:

```
Current User
        ↓
Is Admin?
        ↓
Yes → Perform Action
No  → 403 Forbidden
```

---

# Remember

Every sensitive endpoint must perform its own authorization check.

**Never trust the application workflow.**
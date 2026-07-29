## Idea

The application trusts **client-supplied data** during profile updates.

A user can modify sensitive fields that should only be controlled by the server.

Example:

```json
{
  "email": "test@mail.com",
  "roleid": 2
}
```

↓

Server updates **both** `email` and `roleid`.

→ Vertical Privilege Escalation

---

## Solution

1. Login.
2. Update your email.
3. Intercept the request.
4. Add:

```json
"roleid": 2
```

5. Send the modified request.
6. Access `/admin`.
7. Delete `carlos`.
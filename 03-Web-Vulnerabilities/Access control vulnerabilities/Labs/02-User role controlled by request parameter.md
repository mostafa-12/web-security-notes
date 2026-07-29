
## Idea

Authorization depends on a **user-controlled parameter** (Cookie, URL Parameter, Hidden Field, ...).

If the parameter is forgeable or modifiable:

```
User Role → Modified by Client
```

→ Unauthorized privilege escalation.

---

## Solution

1. Login (`wiener:peter`)
2. Enable **Intercept Response** in Burp.
3. Intercept the login response.
4. Modify:
   ```
   Admin=false
        ↓
   Admin=true
   ```
5. Forward the response.
6. Browse to `/admin`.
7. Delete user `carlos`.
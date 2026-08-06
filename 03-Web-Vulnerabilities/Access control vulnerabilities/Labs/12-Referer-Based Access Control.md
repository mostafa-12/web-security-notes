
**The application uses the `Referer` header as the access control mechanism instead of validating the user's role on the server.**

---

# Defect

The endpoint `/admin-roles` checks whether the request came from `/admin` by inspecting the `Referer` header.

Since the `Referer` header is fully controlled by the client, an attacker can forge it and bypass the access control.

---

# Lab SOL

1. Login as `administrator`.
2. Go to **Admin Panel**.
3. Promote `carlos` and capture the request in **Burp Repeater**.
4. Login as `wiener`.
5. Visit:

```
/admin-roles?username=carlos&action=upgrade
```

Notice that the server returns **Unauthorized** because the request has **no Referer header**.

6. Copy `wiener`'s session cookie into the captured admin request.
7. Change:

```
username=carlos
```

to

```
username=wiener
```

8. Replay the request.

The server accepts the request because it only verifies the `Referer` header, not the user's actual privileges.
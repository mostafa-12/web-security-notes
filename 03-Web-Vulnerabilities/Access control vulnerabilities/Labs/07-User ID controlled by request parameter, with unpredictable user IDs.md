## Idea

The application uses a GUID instead of a predictable identifier, but the authorization logic is still broken.

```
/my-account?id=123
```

↓

```
/my-account?id=9f4b7e8b-bfd3-4d71-9a9d-3cb1f8f6e9f2
```

Changing the identifier is still enough to access another user's resource.

→ Unpredictable Identifier ≠ Secure Authorization

---

The application attempts to prevent IDOR by replacing sequential IDs with random GUIDs. While this makes identifiers difficult to guess, it does **not** enforce authorization.

If an attacker can obtain another user's GUID from any public functionality (profile pages, blog posts, API responses, etc.), they can still replace their own identifier with the victim's identifier.

The backend still performs something conceptually similar to:

```python
user = db.get_user(request.args["id"])
return render_profile(user)
```

instead of verifying that:

```python
owns_resource(current_user, request.args["id"])
```

The vulnerability is therefore still an **IDOR**, because the server trusts a client-controlled resource identifier without checking ownership.

---

## Solution

1. Find any functionality that exposes Carlos's GUID.

Example:

```
Blog Post

↓

Author Profile

↓

?id=<Carlos_GUID>
```

2. Save Carlos's GUID.

3. Login as:

```
wiener:peter
```

4. Visit:

```
/my-account?id=<Your_GUID>
```

5. Replace it with:

```
/my-account?id=<Carlos_GUID>
```

6. Retrieve Carlos's API Key and submit it.

---

> **Mental Model**
>
> Random identifiers are **not** an access control mechanism.
>
> Always ask:
>
> - Can I discover another user's identifier?
> - Is the identifier returned by any public feature?
> - Does changing the identifier alone expose another user's resource?
>
> If the answer is yes, the application is still vulnerable to **Horizontal Privilege Escalation (IDOR)**.

**Category:** Broken Access Control → Horizontal Privilege Escalation → IDOR
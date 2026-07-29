
## Idea

A Horizontal Privilege Escalation can become a Vertical Privilege Escalation when the target **resource belongs to an administrator**.

```
Your Account

↓

Administrator Account
```

↓

```
Administrator Credentials
```

↓

```
Login as Administrator
```

↓

```
Administrative Privileges
```

→ Horizontal Access → Vertical Privilege Escalation

---

The application uses a client-controlled identifier to determine which user's account page to display.

Although users should only be able to access their own account page, the server fails to verify ownership before returning the requested resource.

In this lab, the account page also contains the user's current password (prefilled in a masked input).

The backend behaves conceptually like:

```python
user = db.get_user(request.args["id"])
return render_profile(user)
```

instead of:

```python
if not owns_resource(current_user, request.args["id"]):
    abort(403)

user = db.get_user(request.args["id"])
return render_profile(user)
```

Because the administrator's account page is accessible, the attacker can obtain the administrator's password, authenticate as the administrator, and gain vertical privileges.

The real vulnerability is **Broken Access Control (IDOR)**.

Password disclosure is only the impact.

---

## Solution

1. Login as:

```
wiener:peter
```

2. Visit:

```
/my-account?id=wiener
```

3. Send the request to Burp Repeater.

4. Replace:

```
id=wiener
```

↓

```
id=administrator
```

5. Retrieve the administrator's password from the response.

6. Login using the administrator account.

7. Delete the user:

```
carlos
```

---

> **Mental Model**
>
> Whenever an IDOR exists, don't stop after accessing another normal user's data.
>
> Always ask:
>
> - Does an administrator account exist?
> - Can I access the administrator's resource?
> - Does that resource disclose credentials, API keys, tokens, emails, or any sensitive information?
> - Can this horizontal access be chained into a vertical privilege escalation?

**Category:** Broken Access Control → Horizontal Privilege Escalation → Vertical Privilege Escalation (via Password Disclosure)
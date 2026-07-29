## Idea

The application identifies which user's data to return using a client-controlled identifier.

```
Logged-in User  : wiener
Request         : GET /my-account?id=wiener
```

↓

```
GET /my-account?id=carlos
```

↓

```
Carlos's Account
```

→ Client-controlled identifier + Missing ownership check = Horizontal Privilege Escalation (IDOR)

---

The vulnerability is not the existence of the `id` parameter itself. The real issue is that the application trusts a user-controlled identifier to determine which resource to return, without verifying that the authenticated user actually owns that resource.

A secure application should make two separate checks:

1. **Authentication**
   - Is the user logged in?

2. **Authorization**
   - Is this user allowed to access the requested resource?

In this lab, only the first check exists.

The backend does something conceptually similar to:

```python
user = db.get_user(request.args["id"])
return render_profile(user)
```

instead of:

```python
if request.args["id"] != current_user.username:
    abort(403)
```

or

```python
if not owns_resource(current_user, request.args["id"]):
    abort(403)
```

As a result, changing the `id` parameter is enough to access another user's account.

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

4. Modify:

```
id=wiener
```

↓

```
id=carlos
```

5. If the application returns Carlos's profile, retrieve his API Key and submit it.

---

> **Mental Model**
>
> Always ask:
>
> - Who decides which resource is returned?
> - Is the resource identifier controlled by the client?
> - Does the server verify ownership before returning the resource?
>
> If changing an identifier allows access to another user's resource, suspect **Horizontal Privilege Escalation (IDOR)**.
## Idea

The application detects unauthorized access and returns a redirect, but sensitive data has already been generated and included in the response body.

```
GET /my-account?id=carlos
```

↓

```
302 Found
Location: /
```

↓

```
Response Body

API Key: xxxxxxxxx
```

→ Authorization check performed too late = Information Disclosure

---

The application attempts to prevent unauthorized access by redirecting the user to another page.

However, the sensitive response has already been generated before the authorization decision is fully enforced.

A vulnerable flow looks conceptually like:

```python
user = db.get_user(request.args["id"])

html = render_profile(user)

if not owns_resource(current_user, user):
    return redirect("/")

return html
```

Instead of:

```python
if not owns_resource(current_user, request.args["id"]):
    abort(403)

user = db.get_user(request.args["id"])
return render_profile(user)
```

The browser follows the redirect automatically, so the leak is usually hidden from normal users. Tools like Burp Suite reveal the original response body.

---

## Solution

1. Login as:

```
wiener:peter
```

2. Send the account request to Burp Repeater.

3. Change:

```
id=wiener
```

↓

```
id=carlos
```

4. Observe the response:

```
302 Found
Location: /
```

5. Don't stop at the status code.

Inspect the entire response body and retrieve Carlos's API Key.

---

> **Mental Model**
>
> Never assume a redirect means no data was leaked.
>
> Always inspect:
>
> - Response Body
> - Response Headers
> - JSON Responses
> - HTML Source
>
> Sensitive information may still be present even when the application redirects the user.

**Category:** Broken Access Control → Horizontal Privilege Escalation → Information Disclosure

Always inspect the full response, not only the status code.
---
## Idea

The Front-end checks the HTTP method,

while the Back-end processes multiple methods the same way.

```
Front-end : POST /admin/delete
Backend   : GET  /admin/delete
```

→ Different HTTP Method interpretation = Access Control Bypass

---

The vulnerability is not in the HTTP method itself. The real issue is how different components of the system enforce access control. A platform (Reverse Proxy, Web Server, WAF, etc.) may restrict access based on specific HTTP methods, while the application either accepts additional methods or treats different methods identically. This inconsistency allows an attacker to bypass platform-level access controls.

In this scenario, the Front-End is responsible for blocking sensitive functionality by HTTP method. For example, it may deny only `POST` requests to an administrative endpoint:

```text
DENY:
POST /admin/deleteUser
```

However, the backend application may process the same endpoint regardless of the HTTP method:

```python
@app.route("/admin/deleteUser", methods=["GET", "POST"])
def delete_user():
    username = request.values["username"]
    ...
```

or simply never verify the request method.

As a result, changing only the HTTP method allows the request to bypass the platform restriction while still reaching the same backend functionality.

---

## Solution

1. Send the original request.

```http
POST /admin/deleteUser
```

→ `403 Forbidden`

2. Replay the same request using another HTTP method.

```http
GET /admin/deleteUser?username=carlos
```

or

```http
HEAD /admin/deleteUser
```

3. If the backend handles the request exactly like `POST`, but the platform only blocks `POST`, the administrative action succeeds.

4. Repeat the same idea with other HTTP methods when appropriate:

```
GET
HEAD
PUT
PATCH
OPTIONS
```

and, in some legacy platforms, even invalid methods if they are internally mapped to `GET`.


> **Mental Model**
>
> Always ask:
>
> - Who enforces the HTTP method restriction?
> - Does the backend require the same method?
> - Do all components interpret the request method identically?
>
> Any mismatch between the platform and the application can lead to an Access Control Bypass.
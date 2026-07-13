#### Why do Cookie Prefixes exist?

Normally, the server **cannot know where a cookie originally came from**.

For example:

```
example.com
├── admin.example.com
├── blog.example.com
└── shop.example.com
```

If a subdomain is compromised, it may try to create or overwrite cookies used by the main application (Session Fixation).

Cookie prefixes tell the **browser** to enforce extra security rules before accepting a cookie.

---

### __Secure-

```http
Set-Cookie: __Secure-session=abc; Secure
```

Requirements:

- Must be set over **HTTPS**
- Must include the `Secure` attribute

**Purpose:** Ensure the cookie is only created through a secure connection.

---

### __Host-

```http
Set-Cookie: __Host-session=abc; Secure; Path=/
```

Requirements:

- HTTPS
- `Secure`
- `Path=/`
- **No `Domain` attribute**

**Purpose:** The cookie belongs only to the current host.

Example:

```
admin.example.com
```

can create:

```
__Host-session
```

But

```
blog.example.com
```

cannot overwrite it.

---

### __Http-

Requirements:

- `Secure`
- `HttpOnly`

**Purpose:** Ensure the cookie was created by the server using the `Set-Cookie` header, not by JavaScript.

---

### __Host-Http-

Combines the protections of both:

- HTTPS
- Secure
- HttpOnly
- Path=/
- No Domain

This is the strongest option for sensitive cookies.

---

### Summary

| Prefix | Protection |
|---------|------------|
| `__Secure-` | HTTPS + Secure only |
| `__Host-` | Bound to a single host (No Domain) |
| `__Http-` | Must be HttpOnly (cannot be set by JavaScript) |
| `__Host-Http-` | All previous protections combined |

> **Pentester Note:** Cookie prefixes don't secure the server themselves. They tell the **browser** to reject cookies that don't satisfy specific security requirements, making attacks like **Session Fixation** more difficult.
 
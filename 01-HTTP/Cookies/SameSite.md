#### What is SameSite?

`SameSite` is a cookie attribute that tells the **browser** when it is allowed to send a cookie.

Its main purpose is to reduce **Cross-Site Request Forgery (CSRF)** attacks and improve user privacy by controlling whether cookies are sent with **cross-site requests**.

---

### What is a Cross-Site Request?

A request is **Cross-Site** when the request is sent from one site to another.

Example:

```
Current Site:
https://evil.com

↓

Request

↓

https://bank.com/transfer
```

Since the request originates from `evil.com` but targets `bank.com`, it is considered a **Cross-Site Request**.

---

### SameSite=Strict

```http
Set-Cookie: session=abc123; SameSite=Strict
```

The browser only sends the cookie if the request originates from the **same site**.

#### Allowed

```
bank.com
   │
   ▼
bank.com/profile
```

✅ Cookie is sent.

#### Blocked

```
evil.com
   │
   ▼
bank.com/transfer
```

❌ Cookie is **NOT** sent.

Even if the user clicks a link from another site to `bank.com`, the cookie is not included in the initial request.

#### Typical Use Cases

- Authentication cookies
- Shopping cart
- Sensitive session data

---

### SameSite=Lax

```http
Set-Cookie: session=abc123; SameSite=Lax
```

Similar to `Strict`, but more user-friendly.

#### Same-Site Requests

```
bank.com → bank.com
```

✅ Cookie is sent.

#### User Clicks a Link from Another Site

```
google.com

↓

<a href="https://bank.com">
```

✅ Cookie is sent because the user intentionally navigated to the site.

#### Automatic Cross-Site Requests

```
<img src="https://bank.com/...">

fetch(...)

Auto-submitted form
```

❌ Cookie is generally **NOT** sent.

#### Typical Use Cases

- Login sessions
- Most websites (default behavior)

---

### SameSite=None

```http
Set-Cookie: session=abc123; SameSite=None; Secure
```

The cookie is sent for **all requests**, including Cross-Site requests.

#### Same Site

✅ Cookie sent.

#### Cross Site

✅ Cookie sent.

#### Used For

- Embedded widgets
- Analytics
- Third-party authentication
- Advertisements
- Cross-site integrations

> **Important:** `SameSite=None` requires the `Secure` attribute. Otherwise, modern browsers reject the cookie.

---

### How SameSite Helps Prevent CSRF

Without SameSite:

```
1. User logs into bank.com
        │
        ▼
Session Cookie stored

        │
        ▼

2. User visits evil.com

        │
        ▼

evil.com sends:

POST https://bank.com/transfer
```

The browser automatically attaches the session cookie.

Result:

```
bank.com thinks the request came from the authenticated user.
```

→ CSRF succeeds.

---

With `SameSite=Strict` (or usually `Lax`):

```
evil.com

↓

POST https://bank.com/transfer
```

The browser **does not send the session cookie**.

Result:

```
bank.com receives an unauthenticated request.
```

→ CSRF attack fails.

---

### Why is Lax the Default?

`Strict` can hurt the user experience.

Example:

Someone sends you:

```
https://bank.com/profile
```

If the session cookie is `Strict`, opening the link from another website won't include the cookie in the initial request, and you may be asked to log in again.

`Lax` provides a good balance:

- Better user experience
- Blocks most common CSRF attacks

Therefore, modern browsers treat cookies as **Lax by default** if `SameSite` is not specified.

---

### Comparison

| SameSite | Same-Site Requests | Link Navigation from Another Site | Cross-Site Requests (fetch, img, iframe, form) |
|-----------|--------------------|-----------------------------------|------------------------------------------------|
| **Strict** | ✅ | ❌ | ❌ |
| **Lax** | ✅ | ✅ | ❌ (Most cases) |
| **None** | ✅ | ✅ | ✅ (Requires `Secure`) |

---

### Pentester Notes

- **SameSite=Strict**
  - Strong CSRF mitigation.
  - Usually used for authentication/session cookies.

- **SameSite=Lax**
  - Default browser behavior.
  - Prevents most common CSRF attacks while maintaining usability.

- **SameSite=None**
  - Cookie is always sent.
  - Must include `Secure`.
  - Check whether the application has **additional CSRF protections**, such as:
    - CSRF Token
    - Origin validation
    - Referer validation


```
Top-level navigation:

Page A
  ↓
Page B

Browser ينتقل فعليًا إلى Page B
```

```
Subresource/background request:

Page A
  │
  └────→ Request إلى Page B

أنت لسه على Page A
```
> **Note:** `SameSite` is an additional browser-level defense, **not** a complete replacement for proper CSRF protection.g testing.**

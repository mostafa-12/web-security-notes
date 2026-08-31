

## Access Token

A short-lived token used to access APIs.

```http
GET /api/profile
Authorization: Bearer <access_token>
```

- Usually short-lived (e.g. 15 min).
    
- Sent with API requests.
    
- If stolen, usable until it expires.
    
- Expiration ≠ Logout.
    

---

## Refresh Token

A longer-lived token used to obtain a **new Access Token** without logging in again.

```http
POST /auth/refresh
Cookie: refreshToken=<refresh_token>
```

- Usually longer-lived than the Access Token.
    
- Normally only sent to the refresh endpoint.
    
- Often stored in an `HttpOnly + Secure` Cookie.
    
- Can be a JWT or an opaque/random token linked to a server-side session.
    

---

## Why Two Tokens?

```text
Access Token
→ Short-lived
→ Used for API requests

Refresh Token
→ Long-lived
→ Used to obtain new Access Tokens
```

Using one long-lived token means that if it is stolen, the attacker can use it for a long time.

---

## Refresh Flow

```text
Login
  ↓
Access Token (A) + Refresh Token (R1)
  ↓
API requests using A
  ↓
A expires
  ↓
POST /auth/refresh + R1
  ↓
Server validates R1
  ↓
New Access Token (B)
```

---

## Refresh Token Rotation


![[Pasted image 20260821101932.png]]

With **Rotation**, every successful refresh:

```text
R1 → R2
R2 → R3
R3 → R4
```

The old Refresh Token becomes invalid.

### Why?

To detect **Refresh Token reuse**.

```text
User:
R1 → /refresh → R1 ❌ + R2 ✅

Attacker later:
R1 → /refresh
      ↓
🚨 Reuse detected
```

The server can revoke the session or take another security action.

> Rotation is mainly a **security mechanism**, not a performance optimization.

---

## HttpOnly ≠ Impossible to Steal

`HttpOnly` means JavaScript cannot read the Cookie:

```javascript
document.cookie
```

But it does **not** guarantee the token can never be compromised.

Other protections include:

```text
HttpOnly
Secure
SameSite
CSRF Protection
Refresh Token Rotation
Server-side Session State
Revocation
```

Also, JavaScript may sometimes cause a request that automatically includes the Cookie without knowing its value.

---

## Cookie Scope

Cookies are controlled by:

```text
Domain
Path
Secure
SameSite
```

Example:

```http
Set-Cookie: refreshToken=R1; Path=/auth/refresh
```

```text
/auth/refresh  → Cookie sent ✅
/api/profile   → Cookie not sent ❌
/api/orders    → Cookie not sent ❌
```

`__Host-` Cookies have special restrictions:

```text
Secure
Path=/
No Domain attribute
```

---

## Quick Comparison

||Access Token|Refresh Token|
|---|---|---|
|Purpose|Access APIs|Get new Access Token|
|Lifetime|Short|Longer|
|Usage|Most API requests|Refresh endpoint|
|Storage|Depends on application|Often HttpOnly Cookie|
|Rotation|Usually no|Can use rotation|
|Represents|API access/permissions|Authenticated session / ability to refresh|

---

## One-Line Summary

> **Access Token = short-lived API access.**  
> **Refresh Token = obtain a new Access Token.**  
> **Rotation = replace the used Refresh Token so reuse of an old/stolen token can be detected.**


## Useful writeup link -> https://dev.to/khaledsaeed18/access-and-refresh-tokens-in-token-based-authentication-2a9o
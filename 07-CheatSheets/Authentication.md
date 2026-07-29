# Authentication CheatSheet

## Table of Contents

- [Overview](#overview)
- [Authentication Flow](#authentication-flow)
- [Common Weaknesses](#common-weaknesses)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Authentication verifies identity. Broken authentication is consistently one of the most impactful vulnerability classes in bug bounty.

---

## Authentication Flow

```
User → Login Page → Server validates credentials
                    ↓
              Creates Session / Issues Token
                    ↓
              Returns Set-Cookie / Response with Token
                    ↓
              Browser stores and sends with every request
```

---

## Common Weaknesses

| Weakness | Description |
|----------|-------------|
| Brute Force | No rate limit or lockout on login |
| Credential Stuffing | Reused passwords across sites |
| Username Enumeration | Different responses for valid/invalid usernames |
| Weak Password Policy | No complexity or length requirements |
| Password Reset Flaws | Predictable reset tokens, email enumeration |
| MFA Bypass | Skip MFA by manipulating request parameters |
| Session Not Invalidated | Old session works after password change |
| Remember Me Token | Predictable or static tokens |
| Default Credentials | Admin/admin, root/root |
| Information Disclosure | "Invalid password" vs "User not found" |

---

## Bug Bounty Notes

- [ ] Can you brute force the login endpoint?
- [ ] Is there username enumeration (different error messages)?
- [ ] Is the password reset token predictable?
- [ ] Can you enumerate email addresses via registration?
- [ ] Are there any API endpoints that don't require authentication?
- [ ] Can you re-use a session after password change?
- [ ] Does the logout actually invalidate the session server-side?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Testing only the login form | Password reset and registration are equally important |
| Ignoring rate limiting | Brute force is still the #1 attack vector |
| Not testing account enumeration | Enumeration enables targeted attacks |

---

## Checklist

```
□ Tested brute force protection (rate limit, lockout)
□ Verified username enumeration (login, registration, password reset)
□ Checked password policy requirements
□ Tested password reset flow (token predictability, email enumeration)
□ Checked session invalidation after password change
□ Tested API endpoints without authentication
□ Checked for default credentials on admin panels
```

---

## References

- [PortSwigger: Authentication](https://portswigger.net/web-security/authentication)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

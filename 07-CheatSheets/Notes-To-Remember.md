# Notes to Remember

## Table of Contents

- [Core Principles](#core-principles)
- [Common Pitfalls](#common-pitfalls)
- [Practical Tips](#practical-tips)
- [Bug Bounty Mindset](#bug-bounty-mindset)
- [References](#references)

---

## Core Principles

> The foundational rules that apply to every test.

- **Never trust client-side validation.** It can be bypassed in seconds with Burp or curl.
- **Every request should be tested independently.** One request can bypass controls that multiple requests cannot.
- **Session != Cookie.** A session is server-side state. A cookie is a transport mechanism.
- **Encoding != Encryption.** Base64 is encoding. Anyone can decode it.
- **Security through obscurity is not security.** Hidden endpoints are still accessible.

---

## Common Pitfalls

> Mistakes that waste time or cause missed findings.

- **Testing only GET requests.** Hidden PUT/DELETE/PATCH endpoints may exist.
- **Ignoring 403 responses.** Bypassing forbidden access = access control vulnerability.
- **Trusting error messages.** Custom error pages may return 200 instead of 404.
- **Forgetting to check HTTP methods.** Access control may only be on GET, not POST.
- **Assuming REST = security.** URL structure does not imply authorization.
- **Not checking OPTIONS.** May reveal hidden endpoints and allowed methods.
- **Ignoring JavaScript files.** They reveal APIs, secrets, and internal logic.
- **Testing with only one user role.** Admin vs regular vs unauthenticated — test all.

---

## Practical Tips

> Lessons learned the hard way.

- **Always check robots.txt first.** It may reveal hidden directories.
- **Decode before validating.** Double-encoded payloads bypass single-decode filters.
- **Test parameter pollution.** Duplicate parameters with different values may change behavior.
- **Check for rate limiting early.** Brute force without rate limits = easy win.
- **Save interesting requests in Repeater.** You'll need them again.
- **Review HTTP History after browsing.** Background requests may reveal hidden endpoints.
- **Test Content-Type switching.** JSON ↔ form-data ↔ XML may bypass validation.
- **Check cookie attributes.** HttpOnly, Secure, SameSite — each missing flag is a finding.
- **Look for CORS misconfigurations.** Access-Control-Allow-Origin with credentials = vulnerability.
- **Test open redirects.** They're easy to find and useful for phishing.

---

## Bug Bounty Mindset

> How to think like a bug bounty hunter.

- **Recon is everything.** Better recon = better findings. Most missed bugs are due to incomplete recon.
- **Test what others skip.** Most hunters test the login form. Few test password reset, registration, and logout.
- **Think like a developer.** Understand the application's logic before testing it.
- **Read error messages carefully.** They leak information about the backend.
- **Chain vulnerabilities.** A low-severity bug combined with another can become critical.
- **Document everything.** Notes from today's test are tomorrow's lead.
- **Quality over quantity.** One well-written report beats ten mediocre ones.
- **Read the program rules carefully.** Out-of-scope testing wastes everyone's time.

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Bug Bounty Methodology](https://www.bugbountyhunting.com/)

# Input Validation CheatSheet

## Table of Contents

- [Overview](#overview)
- [Validation Approaches](#validation-approaches)
- [Client-Side vs Server-Side](#client-side-vs-server-side)
- [Boundary Validation](#boundary-validation)
- [Canonicalization](#canonicalization)
- [Output Encoding](#output-encoding)
- [Parameterized Queries](#parameterized-queries)
- [Common Bypasses](#common-bypasses)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Input validation is the first line of defense against injection attacks. Never trust user input — validate, sanitize, and encode.

---

## Validation Approaches

| Approach | Description | Example |
|----------|-------------|---------|
| Whitelist | Allow only known-good input | `^[a-zA-Z0-9]+$` |
| Blacklist | Block known-bad input | Reject `<script>` |

> **Whitelist is always preferred.** Blacklists are trivially bypassed.

---

## Client-Side vs Server-Side

| | Client-Side | Server-Side |
|--|-------------|-------------|
| Location | JavaScript in browser | Application backend |
| Speed | Instant feedback | Requires request |
| Security | ❌ Trivially bypassed | ✅ Cannot be bypassed |
| Purpose | UX improvement | Actual security |

> **Never rely on client-side validation alone.** Every check can be bypassed with Burp, curl, or browser dev tools.

---

## Boundary Validation

> Validate data at every trust boundary, not only at input.

```
User Input → [Boundary 1] → App Logic → [Boundary 2] → Database
                 ↑                              ↑
           Validate here                  Validate here
```

### Why?

- Each component has different security requirements
- Data may change format during processing
- A single validation point is not enough

---

## Canonicalization

> Convert encoded/obfuscated input to its standard form before validating.

| Attack | Example |
|--------|---------|
| Directory traversal | `..%2f..%2fetc/passwd` |
| Double encoding | `%252e%252e%252f` |
| Unicode normalization | `＜script＞` → `<script>` |

### Rules

1. Always validate the **canonical (decoded)** form
2. Decode **before** validating, not after
3. Apply multiple decode passes if encoding layers exist

---

## Output Encoding

> Encode data based on where it will be used.

| Context | Encoding |
|---------|----------|
| HTML body | HTML entity encoding (`<` → `&lt;`) |
| HTML attribute | Attribute encoding |
| JavaScript | JS encoding (`\x3c`) |
| URL | URL encoding (`%3C`) |
| CSS | CSS encoding |
| SQL | Parameterized queries (not encoding) |
| XML | XML encoding |

> **The encoding must match the context.** HTML-encoding in JavaScript context is still vulnerable.

---

## Parameterized Queries

> Use prepared statements to separate SQL logic from data.

### Vulnerable

```sql
SELECT * FROM users WHERE id = '$id'
```

### Secure

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
```

### ORMs

ORMs (SQLAlchemy, Hibernate, Eloquent) use parameterized queries by default. However:

- Raw queries in ORMs are still vulnerable
- `ORM.filter(raw_input)` may be unsafe
- Always check for raw query methods

---

## Common Bypasses

| Bypass | Description |
|--------|-------------|
| Case variation | `<ScRiPt>` vs `<script>` |
| Encoding | `&#60;script&#62;` |
| Null bytes | `<script%00>` |
| Double encoding | `%253Cscript%253E` |
| Parameter pollution | Duplicate parameters with different values |
| Content-Type switch | JSON ↔ form-data ↔ XML |
| Unicode | Full-width characters, homoglyphs |

---

## Bug Bounty Notes

- [ ] Is input validated on the client-side only?
- [ ] Can you bypass blacklists with encoding/case variation?
- [ ] Is the application vulnerable to SQL injection (try all input fields)?
- [ ] Can you inject into HTML/JavaScript contexts (XSS)?
- [ ] Does the application normalize paths before validation (traversal)?
- [ ] Can you switch Content-Type to bypass validation?
- [ ] Are there any raw SQL queries in the ORM layer?
- [ ] Can you inject into HTTP headers (CRLF injection)?
- [ ] Is XML input accepted (XXE potential)?
- [ ] Can you upload files with unexpected extensions?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Relying on client-side validation | Bypassed in seconds with Burp |
| Using blacklist filtering | Trivially bypassed with encoding |
| Validating before canonicalization | Encoding hides malicious payloads |
| HTML-encoding everywhere | Context matters — JavaScript context needs JS encoding |
| Trusting ORM to be secure | Raw queries in ORM are still vulnerable |

---

## Checklist

```
□ Verified server-side validation exists on all inputs
□ Tested client-side validation bypass
□ Tested SQL injection on all input fields
□ Tested XSS in all output contexts (HTML, attribute, JS, URL)
□ Tested path traversal with encoding bypasses
□ Tested Content-Type switching (JSON ↔ form-data ↔ XML)
□ Tested header injection (CRLF)
□ Tested file upload with malicious extensions
□ Verified parameterized queries are used for DB access
□ Tested XML input for XXE
```

---

## References

- [PortSwigger: Input Validation](https://portswigger.net/web-security/sql-injection)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

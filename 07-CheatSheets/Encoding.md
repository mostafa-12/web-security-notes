# Encoding CheatSheet

## Table of Contents

- [Overview](#overview)
- [URL Encoding](#url-encoding)
- [HTML Encoding](#html-encoding)
- [Unicode](#unicode)
- [Base64](#base64)
- [Hex Encoding](#hex-encoding)
- [JSON Escaping](#json-escaping)
- [Double Encoding](#double-encoding)
- [Encoding for Security Testing](#encoding-for-security-testing)
- [Bug Bounty Notes](#bug-bounty-notes)
- [Common Mistakes](#common-mistakes)
- [Checklist](#checklist)
- [References](#references)

---

## Overview

> Encoding transforms data into a different format. In web security, encoding is used both for data transport and for bypassing input filters.

---

## URL Encoding

| Character | Encoded | Description |
|-----------|---------|-------------|
| Space | `%20` or `+` | Space separator |
| `&` | `%26` | Query string separator |
| `=` | `%3D` | Parameter assignment |
| `/` | `%2F` | Path separator |
| `#` | `%23` | Fragment identifier |
| `%` | `%25` | Escape character |
| `?` | `%3F` | Query string start |
| `<` | `%3C` | HTML tag |
| `>` | `%3E` | HTML tag |
| `"` | `%22` | Attribute value |

### When to Use

- Sending special characters in URLs
- Bypassing URL-based input filters
- Directory traversal payloads

### Examples

```
# Space
hello%20world

# Directory traversal (encoded)
..%2F..%2F..%2Fetc%2Fpasswd

# HTML in URL (encoded)
%3Cscript%3Ealert(1)%3C%2Fscript%3E
```

---

## HTML Encoding

| Character | Encoded |
|-----------|---------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |

### When to Use

- Preventing XSS in HTML context
- Output encoding for dynamic content

### Example

```html
<!-- Vulnerable -->
<script>document.write(userInput)</script>

<!-- Secure (HTML encoded) -->
&lt;script&gt;alert(1)&lt;/script&gt;
```

---

## Unicode

| Format | Example |
|--------|---------|
| `\uXXXX` | `\u003c` = `<` |
| `\xXX` | `\x3c` = `<` |
| Full-width | `＜` (U+FF1C) = `<` |
| Homoglyphs | `꜀` (U+A700) vs `c` |

### When to Use

- Bypassing blacklist filters
- Obfuscating payloads
- Unicode normalization attacks

### Examples

```
# Unicode-encoded XSS
\u003cscript\u003ealert(1)\u003c/script\u003e

# Full-width characters (bypasses some filters)
＜script＞alert(1)＜/script＞
```

---

## Base64

| Input | Encoded |
|-------|---------|
| `A` | `QQ==` |
| `AB` | `QUI=` |
| `ABC` | `QUJD` |
| `{"user":"admin"}` | `eyJ1c2VyIjoiYWRtaW4ifQ==` |

### When to Use

- Tokens, cookies, Basic Auth
- Obfuscating data in transit
- JWT payloads

### Decode

```bash
echo "eyJ1c2VyIjoiYWRtaW4ifQ==" | base64 -d
# Output: {"user":"admin"}
```

> **Base64 is encoding, NOT encryption.** Always try decoding it.

---

## Hex Encoding

| Input | Hex |
|-------|-----|
| `A` | `41` |
| `AB` | `4142` |
| `<` | `3c` |

### When to Use

- URL-encoded hex: `%3c` = `<`
- Binary data representation
- Some WAF bypass techniques

---

## JSON Escaping

| Character | Escaped |
|-----------|---------|
| `"` | `\"` |
| `\` | `\\` |
| `/` | `\/` |
| `\n` | `\\n` |
| `\t` | `\\t` |
| Unicode | `\u003c` |

### Example

```json
{"name": "Ahmed \"Admin\""}
{"path": "..\/..\/etc\/passwd"}
```

---

## Double Encoding

> Encoding an already-encoded string.

| Single Encoded | Double Encoded |
|---------------|----------------|
| `%2F` (`/`) | `%252F` |
| `%3C` (`<`) | `%253C` |
| `%27` (`'`) | `%2527` |

### When to Use

- Bypassing filters that decode once
- IIS path traversal bypass

```
# First decode: %252F → %2F
# Second decode: %2F → /
# Result: traversal payload
```

---

## Encoding for Security Testing

| Test | Encoding Technique |
|------|-------------------|
| XSS filter bypass | HTML encode, unicode, double encode |
| SQL injection bypass | URL encode, unicode, double encode |
| Path traversal bypass | URL encode, double encode, unicode |
| WAF bypass | Mixed encoding, case variation |
| Authentication bypass | Base64, URL encode in headers |

### Burp Decoder Shortcuts

| Action | Shortcut |
|--------|----------|
| URL encode | `Ctrl+U` |
| URL decode | `Ctrl+Shift+U` |
| Base64 encode | `Ctrl+B` |
| Base64 decode | `Ctrl+Shift+B` |

---

## Bug Bounty Notes

- [ ] Can you decode Base64 tokens to find sensitive data?
- [ ] Can you bypass input filters with encoding?
- [ ] Are there any double-encoding vulnerabilities?
- [ ] Can you use Unicode to bypass blacklist filters?
- [ ] Can you use URL encoding to bypass path restrictions?
- [ ] Does the application properly decode input before processing?
- [ ] Can you inject via JSON encoding in API parameters?

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Thinking Base64 is encryption | It's encoding — always decodable |
| Encoding after validation | Validate the decoded form |
| Using HTML encoding everywhere | Each context needs its own encoding |
| Ignoring double encoding | Filters may decode only once |

---

## Checklist

```
□ Decoded all Base64 tokens (cookies, JWT, API keys)
□ Tested URL encoding for filter bypass
□ Tested HTML encoding for XSS filter bypass
□ Tested double encoding for path traversal
□ Tested Unicode for blacklist bypass
□ Verified application decodes input before processing
□ Tested JSON encoding in API parameters
□ Checked for hex-encoded payloads
```

---

## References

- [PortSwigger: Encoding](https://portswigger.net/web-security)
- [OWASP Encoding Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html)

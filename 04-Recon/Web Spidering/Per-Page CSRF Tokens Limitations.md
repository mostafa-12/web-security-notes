
## Per-Page CSRF Tokens

Some applications generate a new CSRF token for each page or form.

### Common Behavior

Most modern applications allow multiple valid CSRF tokens at the same time.

Example:

```text
GET /page1  -> CSRF = A

GET /page2  -> CSRF = B

POST /page1 (csrf=A) ✅ Accepted
```

The old token (`A`) is still valid for its original form.

### Strict Implementations

Some applications invalidate previously issued tokens whenever a new one is generated.

Example:

```text
GET /page1  -> CSRF = A

GET /page2  -> CSRF = B

POST /page1 (csrf=A) ❌ Invalid CSRF Token
```

In this case, only the most recently issued token remains valid.

### Impact on Spidering

An automated spider may request many pages before submitting any forms.

If the application invalidates older tokens, previously collected forms may fail because their CSRF tokens have expired.

> This behavior is application-specific and is **not** how most modern web applications implement CSRF protection.




## HTTP Headers

### General Headers
Used to describe the HTTP message itself.

- Connection → Keep/Close TCP connection.
- Content-Type → Type of message body (HTML, JSON, etc.).
- Content-Length → Body size in bytes.
- Content-Encoding → Compression (gzip, br).
- Transfer-Encoding → How the body is transferred (e.g., chunked).
### Common Request Headers

- Host → Target host.
- User-Agent → Client information.
- Referer → Previous page.
- Cookie → Send stored cookies.
- Accept → Accepted response types.
- Accept-Encoding → Accepted compression methods.
- Authorization → Authentication credentials.
- Origin → Source origin (important for CORS).

### Common Response Headers

- Set-Cookie → Issue cookies.
- Server → Server information.
- Location → Redirect target.
- Cache-Control / Expires / Pragma → Cache behavior.
- Access-Control-Allow-Origin → CORS policy.
- ETag → Resource version (Caching).
- WWW-Authenticate → Authentication challenge.
- X-Frame-Options → Clickjacking protection.


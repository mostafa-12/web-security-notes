### Cookie Attributes

- **Expires** → Cookie expiration date.
	- If omitted → Session Cookie (deleted when the browser session ends).

- **Domain** → Specifies which domain/subdomains can receive the cookie.

- **Path** → Specifies which URL paths can receive the cookie.

- **Secure** → Cookie is sent only over HTTPS.

- **HttpOnly** → Prevents JavaScript (`document.cookie`) from accessing the cookie, helping mitigate cookie theft via XSS.
 
- [Samesite Attribute](/01-HTTP/Cookies/SameSite) -> is a cookie attribute that tells the **browser** when it is allowed to send a cookie.
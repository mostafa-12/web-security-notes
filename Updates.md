 
# Learning Log

---

## 2026-07-14

###  Completed

#### Web Application Hacker's Handbook

- ✅ Chapter 3 — Web Application Technologies

#### MDN HTTP

Studied and documented:

- HTTP Messages
- HTTP Methods
- HTTP Headers
- Status Codes
- Cookies
- Cookie Attributes
- SameSite
- Cookie Prefixes
- Privacy & Tracking
- HTTPS
- Proxy Authentication
- State & Sessions
- DOM
- Ajax
- JSON
- Encoding Schemes

---

### 💡 Key Concepts I Finally Understood

- How Burp Proxy performs a Man-in-the-Middle attack using two independent TLS connections.
- Why Burp generates its own certificate instead of reusing the server's certificate.
- Why Certificate Pinning breaks Burp interception.
- Difference between a Session and a Session ID.
- How SameSite mitigates CSRF attacks.
- Why `__Host-` cookies help prevent Session Fixation.
- Difference between First-Party and Third-Party Cookies.
- HTTP/2 changes the transport format (binary framing), not HTTP semantics.

---

### 🛠 Repository Improvements

- Reorganized the HTTP notes into dedicated topics.
- Split Cookies into multiple focused notes:
  - Attributes
  - SameSite
  - Cookie Prefixes
- Added an HTTP knowledge base structure.
- Improved note organization for future expansion.

---

### 📖 Next Goal

- Chapter 4 - The Web Application Hacker's Handbook
- Begin studying **Access Control**.
- Start solving PortSwigger Access Control labs alongside the theory.
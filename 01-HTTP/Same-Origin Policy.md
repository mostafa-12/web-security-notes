## Same-Origin Policy (SOP)

### What it prevents

#### 1. Cross-Origin Requests
- A page **can send** requests to another domain.
- It **cannot read** the response.
- This behavior is the reason attacks like **CSRF** are possible, while many of them remain **blind**.

#### 2. Cross-Origin Scripts
- A page can load JavaScript from another domain using `<script src="...">`.
- The loaded script executes with the **permissions of the current page**, not the domain it came from.
- Security risks:
  - Supply Chain Attack
  - Third-Party Script compromise
  - JSONP abuse (legacy)
  - XSS if the attacker controls the script source

#### 3. Cookies & DOM Isolation
A page **cannot** access another domain's:
- Cookies
- DOM
- Local Storage
- Session Storage

This prevents websites from stealing or modifying data belonging to other origins.

### Remember

SOP protects **reading data**, not necessarily **sending requests**.
Send ✅ | Read ❌ | Execute External JS ✅ | Access Other Origin Data ❌

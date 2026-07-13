## State & Sessions

### Why?

HTTP is **stateless**.
Each request is independent, so the server does not remember previous requests.

To implement features like:
- Authentication
- Shopping Cart
- Checkout
- Multi-step Forms

the application must maintain the user's **State**.

---

### What is State?

State = Information the application needs to remember about a user.

Examples:
- Logged in or not
- Shopping cart contents
- User role
- Current checkout step

---

### What is a Session?

A **Session** stores a user's state across multiple HTTP requests.

Typical flow:
1. User logs in.
2. Server creates a Session.
3. Server generates a unique **Session ID**.
4. Session ID is sent to the browser (usually in a Cookie).
5. Browser sends the Session ID with every request.
6. Server retrieves the correct Session using that ID.

---

### Where is the State Stored?

#### Server-side (Most Common)

State is stored on the server.

Browser stores only:
- Session ID

**Pros:**
- More secure.
- Client cannot directly modify the session data.

---

#### Client-side

State is stored on the client.

Examples:
- Hidden Fields
- ASP.NET ViewState
- JWT (depending on implementation)

**Risks:**
- Client can modify the data.

**Protection:**
- Signatures (Integrity)
- Encryption (when needed)

---

### Flask Comparison

#### Flask Default

- Session data is stored inside a **signed Cookie**.
- Cookie is signed using `SECRET_KEY`.
- User can read the cookie.
- User **cannot modify** it without breaking the signature.

#### Flask-Session

- Session data is stored on the server.
- Browser stores only the **Session ID**.
- Similar to the traditional server-side session model described in the book.

---

### Remember

- **HTTP** → Stateless
- **State** → Information the application needs to remember.
- **Session** → Stores the user's state.
- **Session ID** → Identifies the correct session (usually sent in a Cookie).

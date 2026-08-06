### Resource

- The resource is a static transcript file stored on the server.
- Each transcript is accessed directly through its URL.
- The filename is a predictable numeric identifier (e.g. `1.txt`, `2.txt`, `3.txt`).

---

### Vulnerability

The application retrieves transcript files directly based on the filename provided in the URL.

There is **no authorization check** to verify whether the requested transcript belongs to the current user.

As a result, an attacker can modify the filename and access transcripts belonging to other users.

---

### Exploitation

1. Open your own transcript.
2. Observe the URL format (`/transcripts/<id>.txt`).
3. Replace the filename with another predictable ID (e.g. `1.txt`).
4. Read another user's transcript.
5. Extract sensitive information (Carlos's password).
6. Log in using the stolen credentials.

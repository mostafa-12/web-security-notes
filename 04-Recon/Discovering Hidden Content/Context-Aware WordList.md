# Context-Aware Brute Force

Brute-force enumeration should become more targeted as more information about the application is discovered.

## Step 1

Discover directories.

Example:

```text
/auth/
/images/
/include/
```

---

## Step 2

Focus on each discovered directory.

Example:

```text
/ auth /

├── Login
├── Logout
├── Register
├── Profile
```

Instead of guessing random names at the application root, generate guesses related to the directory's purpose.

---

## Analyzing Responses

Useful indicators include:

- HTTP Status Code
- Response Length
- Response Time

Sorting responses by these values makes interesting resources easier to identify.

---

## Status Code Example

```text
200 OK
```

The resource exists and is accessible.

```text
302 Found
Location: /auth/Login
```

The resource exists but requires authentication.

```text
404 Not Found
```

The resource does not exist.

---

## Key Idea

Every discovery provides additional context.

The more you understand the application's structure, the smarter your enumeration becomes.

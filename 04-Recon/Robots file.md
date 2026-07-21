## robots.txt

The `robots.txt` file tells search engines which paths should not be indexed.

Example:

```text
User-agent: *
Disallow: /admin
Disallow: /backup
```

### Important

- It does **not** prevent direct access.
- It may reveal hidden or sensitive directories.
- A link-based spider may not discover these paths unless they are referenced elsewhere.

---

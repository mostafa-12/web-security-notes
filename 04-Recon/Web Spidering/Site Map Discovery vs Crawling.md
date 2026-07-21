## Site Map Discovery vs Crawling

A proxy/spider parses **only the HTTP responses it receives**.

Example:

```text
GET /
```

Response:

```html
<a href="/admin">
<script src="/static/app.js">
```

The spider can discover:

- `/admin`
- `/static/app.js`

However, it **has not analyzed** `/admin` yet because no request has been made to it.

To analyze `/admin`, a request must be sent:

```text
GET /admin
```

Only then can the spider parse its response and discover additional content.

---

### User-Directed Spidering Workflow

```text
Visit a page
      │
      ▼
Spider parses the response
      │
      ▼
New links/resources are discovered
      │
      ▼
Visit those resources manually
      │
      ▼
Spider parses their responses
      │
      ▼
Discover even more content
```

This process is repeated until no new content is found.

> A discovered URL is **not** the same as a crawled URL.

---

### Why Review the Site Map?

The generated Site Map may contain URLs that were discovered but never visited.

Example:

```text
/
└── /admin      ← Discovered only
```

Visiting `/admin` manually allows the spider to analyze its response and expand the Site Map further.

This is why the recommended workflow is:

1. Browse manually.
2. Review the Site Map.
3. Visit newly discovered resources.
4. Repeat.

---


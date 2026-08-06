
# Build the Minimum Request

Reduce the request to only the required components.

Remove unnecessary:

- Headers
- Parameters
- Cookies
- Body fields

The smaller the request, the easier it becomes to understand the server behavior.

---

# Observe → Hypothesize → Test

Every access control test should follow this cycle.

```
Observe
      ↓
Hypothesize
      ↓
Test
      ↓
Observe Again
```

Example:

```
There is a Referer header.

↓

Maybe the server validates it.

↓

Remove it.

↓

Modify it.

↓

Compare the responses.
```

---

# Isolate Variables

Never modify multiple things in the same request.

Bad:

- Change Cookie
- Change Referer
- Change Method

↓

Response changes

Unknown cause.

Good:

Modify only one variable.

Example:

```
Referer = /admin
↓

200 OK

Referer = google.com
↓

403

No Referer
↓

403
```

Now there is strong evidence that the application validates the Referer header.

---

# Read Responses Carefully

Responses often reveal:

- Hidden parameters
- Confirmation steps
- Hidden endpoints
- Internal workflow
- Error messages
- Technology stack

Example:

```html
<input
type="hidden"
name="confirmed"
value="true">
```

This reveals another step in the workflow.

---

# Never Trust Client-Controlled Data

Always investigate whether the server trusts:

- URL Parameters
- POST Parameters
- Cookies
- Referer
- Origin
- User-Agent
- X-Forwarded-For

If any of them affects authorization, there may be a vulnerability.

---

# Pentester Mindset

```
Observe
      ↓
Understand
      ↓
Build Minimum Request
      ↓
Create Hypothesis
      ↓
Modify ONE Variable
      ↓
Observe Again
      ↓
Repeat
```
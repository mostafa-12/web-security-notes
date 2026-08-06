
### Multi-Step Workflows in HTTP

Many sensitive actions are not executed immediately.

**Instead, the application splits the process into multiple HTTP requests.**

Example:

```text
POST /admin-roles
        │
        ▼
Return Confirmation HTML Page
        │
        ▼
User clicks "Yes"
        │
        ▼
POST /admin-roles
confirmed=true
        │
        ▼
Sensitive Action Executes
```

---

### Why did a POST request return HTML?

The HTTP method **does not determine the response type**.

A POST request can return:

- HTML
- JSON
- XML
- Redirect (302)
- Empty Response (204)

In this case, the server returned an HTML page asking the user to confirm the action.

---

### Where did `confirmed=true` come from?

The server generated an HTML form containing hidden inputs.

Example:

```html
<form action="/admin-roles" method="POST">

<input type="hidden" name="action" value="upgrade">
<input type="hidden" name="confirmed" value="true">
<input type="hidden" name="username" value="carlos">

</form>
```

When the user clicks **Yes**, the browser automatically submits those hidden fields in a new POST request.

---

### Why is this interesting for a Pentester?

Responses often reveal the application's internal workflow.

By reading the HTML response, you can discover:

- Additional endpoints
- Hidden parameters
- Multi-step processes
- Confirmation flags
- Hidden form fields
- Application logic

Never inspect only the requests.

Always analyze the responses carefully.
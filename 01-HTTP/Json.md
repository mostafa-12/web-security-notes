## JSON (JavaScript Object Notation)

- JSON is a lightweight data-interchange format.
- It is the most common format used by modern Ajax applications.
- JavaScript can parse JSON directly into objects.
- A typical Ajax flow:
    - User Action
    - Ajax Request
    - Server returns JSON
    - JavaScript updates the DOM

### Example Response

```json
{
    "name": "Mike Kemp",
    "id": "8041148671",
    "email": "mike@example.com"
}
```

### Pentesting Notes

- JSON may appear:
    - As the entire request body (`application/json`)
    - Inside a normal form parameter (`application/x-www-form-urlencoded`)
- Always inspect and modify JSON values in Burp, as they often contain user-controlled data.



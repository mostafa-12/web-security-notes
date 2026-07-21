# Hidden Content Discovery Methodology

## 1. Learn Normal vs Invalid Responses

Before automation, manually request:

- A valid resource
- An invalid resource

Understand how the application responds to non-existing paths.

Example:

```text
/login        → 200 OK
/random123    → 404 Not Found
```

Some applications return:

```text
/random123    → 200 OK
```

with a custom "Page Not Found" page.

---

## 2. Start from the Site Map

Use previously discovered directories as enumeration targets.

Example:

```text
/auth/
/api/
/images/
```

---

## 3. Perform Targeted Brute Force

Generate requests using context-aware wordlists.

Example:

```text
/auth/Login
/auth/Register
/auth/Profile
```

---

## 4. Analyze Responses

Review responses using indicators such as:

- Status Code
- Response Length
- Response Time

Filter common "Not Found" responses to focus on interesting results.

---

## 5. Enumerate Recursively

Every newly discovered directory becomes a new target for enumeration.

```text
/auth
   │
   ├── Register
   ├── Profile
   └── Admin

↓

Enumerate each newly discovered location.
```

## Key Idea

Hidden content discovery is an iterative process.

Every discovery provides new information that guides the next round of enumeration.


# Hidden Content Discovery Workflow

## 1. Build a Knowledge Base

Collect all discovered:

- Directories
- Files
- Extensions
- IDs
- URL Patterns

---

## 2. Identify Naming Conventions

Examples:

```text
AddUser
ViewUser
```

↓

```text
EditUser
DeleteUser
```

Use existing names to predict new resources.

---

## 3. Look for Sequential Patterns

Examples:

```text
Report2024.pdf
Report2025.pdf
```

↓

```text
Report2026.pdf
```

---

## 4. Analyze Client-Side Resources

Review:

- HTML
- JavaScript
- HTML Comments
- Disabled Forms

These may reveal hidden endpoints or internal functionality.

---

## 5. Expand Wordlists

Try alternative extensions:

```text
.bak
.old
.tmp
.txt
.src
.java
.cs
```

---

## 6. Search for Temporary Files

Examples:

```text
.DS_Store
.tmp
file.php~
```

---

## 7. Generate Smart Combinations

Combine:

- Directories
- File names
- Extensions

Instead of random guessing.

---

## 8. Perform Context-Aware Enumeration

Generate new requests based on observed naming conventions rather than generic wordlists.

---

## 9. Repeat Recursively

Every new discovery becomes the basis for further:

- Spidering
- Pattern analysis
- Content discovery
- Enumeration






# Automated Web Server Scanners

## Limitations

Automated scanners may produce:

- False Positives
- False Negatives
- Redundant checks

---

## Common Causes

- Hidden server banners
- Custom directory locations
- Custom error pages
- Different HTTP response behavior

---

## Best Practice

Always verify scanner findings manually.

Raw response information is often more reliable than the scanner's conclusions.

---

## Domain vs IP

Many applications use virtual hosting.

When scanning, prefer the correct hostname instead of only the server IP to ensure all application links are followed correctly.

# Application Pages vs Functional Paths

## Traditional Model

Each URL represents a unique application function.

Example:

```text
/login
/profile
/orders
```

Request parameters provide **data**, not functionality.

Example:

```text
/profile?id=15
```

- Function → `/profile`
- Data → `id=15`

---

## Functional Path Model

Some applications expose all functionality through a single endpoint.

Example:

```http
POST /bank.jsp
```

The function is determined by request parameters.

```text
servlet=TransferFunds
method=confirmTransfer
```

Here:

- URL → Entry point
- Parameters → Function
- Remaining parameters → Data

---

## Why It Matters

A URL-based site map may completely hide the application's real functionality.

Instead, mapping should focus on:

- Application workflows
- Functional paths
- Relationships between actions

---

## Key Idea

Map **what the application does**, not only **where requests are sent**.

# Enumerating Function-Based Applications

## Step 1

Identify how the application selects functionality.

Examples:

```text
/admin/editUser.jsp
```

vs

```text
/admin.jsp?action=editUser
```

---

## Step 2

Adapt content discovery to the application's design.

Instead of brute-forcing URLs:

```text
/admin/
/users/
/login/
```

Brute-force function identifiers:

```text
action=login
action=logout
action=editUser
```

or

```text
servlet=TransferFunds
method=confirmTransfer
```

---

## Step 3

Identify valid function names by observing response differences between:

- Invalid function names
- Valid functions with invalid parameters

Look for response patterns that indicate a valid function.

---

## Step 4

Create a Functional Map instead of only a URL map.

Example:

Login
↓
Dashboard
↓
Transfer Funds
↓
Confirm Transfer

---

## Key Idea

Always enumerate the component that actually determines application functionality, whether it is:

- URL
- Parameter
- Method
- Action
- Servlet
# Discovering Hidden Parameters

## Concept

Applications may contain undocumented parameters that change application behavior.

These parameters are often not referenced anywhere in the application's visible content.

---

## Examples

```text
debug=true
```

Possible effects:

- Enable debug mode
- Disable validation
- Bypass restrictions
- Show verbose errors

---

## Discovery Method

Brute-force:

- Parameter names
- Parameter values

Example:

```text
debug=true
test=1
verbose=yes
```

---

## Response Analysis

Look for differences such as:

- Response length
- Status code
- Headers
- Cookies
- Error messages
- Redirects

---

## Prioritize Sensitive Functions

Focus on areas such as:

- Login
- Search
- File upload
- File download

---

## Key Idea

Applications may hide functionality behind undocumented request parameters rather than hidden URLs.
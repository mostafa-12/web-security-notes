
# Phase 1 - Understand the Application

Before testing Access Control, the first objective is **understanding how the application is intended to work**.

## Goal

Build a mental model of the application's authorization system.

Ask yourself:

- What user roles exist?
- What can each role do?
- What resources belong to each user?
- What actions are restricted?
- Are there any multi-step workflows?
- What are the business rules?

During this phase, use the application as a normal user.

Explore every page, button, menu, and feature until you understand the application's expected behavior.

> If you don't know how the application is supposed to behave, you won't recognize when access control is broken.

---

## Mentality

Don't look for vulnerabilities yet.

First, learn the application.

The goal is to understand:

> **What should happen?**

Only after understanding the intended behavior should you start asking:

> **Can I do something I'm not supposed to do?**



# Phase 2 - Identify Attack Surface

Once you understand how the application works, start identifying potential authorization targets.

At this stage, don't immediately attack the application.

Instead, observe.

## Look for

### Resources

- User profiles
- Orders
- Messages
- Files
- Notes
- Billing
- Admin panels

---

### Identifiers

Look for anything that identifies a resource.

Examples:

- id
- uuid
- username
- email
- filename

Simply finding identifiers does **not** indicate a vulnerability.

It tells you **what may become testable later**.

---

### Workflows

Observe any multi-step functionality.

Examples:

- Checkout
- Password Reset
- Registration
- MFA
- Account Recovery

Ask:

> Can these steps be skipped or reordered?

---

### HTTP Requests

Analyze every request.

Ask yourself:

- What parameters identify the resource?
- What parameters identify the user?
- What information might be used during authorization?
- Which values are supplied by the client?

---

## Mentality

During this phase you are **collecting hypotheses**, not proving vulnerabilities.

Think like this:

"I found an interesting parameter."

NOT

"I found a vulnerability."

Every observation becomes a future test case.



# Phase 3 - Testing Authorization

At this stage, you should already understand:

- How the application works.
- The application's authorization model.
- Sensitive functionality.
- Interesting requests and resources.

Now it's time to verify whether the server correctly enforces authorization.

---

## Step 1 - Choose a Target

Select one sensitive functionality at a time.

Examples:

- Profile
- Account Settings
- Admin Panel
- Billing
- Orders
- User Management
- Password Change
- File Download
- API Endpoint

Avoid testing everything randomly.

Always focus on a single target.

---

## Step 2 - Identify the Authorization Model

Ask yourself:

- Who should be allowed to access this?
- Who should NOT be allowed?
- Is this:
    - Horizontal Access Control?
    - Vertical Access Control?
    - Context-dependent Access Control?

Understanding the expected behavior is essential before attempting to bypass it.

---

## Step 3 - Test the Authorization Decision

Attempt to access or perform actions that should not be permitted.

Depending on the target, test things such as:

### Horizontal Access Control

Can another user access this resource?

Examples:

- Change ID
- Change UUID
- Change Username
- Change Email

---

### Vertical Access Control

Can a lower privileged user perform privileged functionality?

Examples:

- Admin pages
- Admin APIs
- Administrative actions

---

### Context-dependent Access Control

Can the application's workflow be bypassed?

Examples:

- Skip required steps
- Repeat completed actions
- Access later stages directly

---

## Step 4 - Try Alternative Requests

If authorization is denied, don't stop.

Try reaching the same functionality differently.

Examples:

### URL Manipulation

- Different capitalization
- Trailing slash
- Different extensions

---

### HTTP Methods

- GET
- POST
- HEAD
- OPTIONS
- PUT
- PATCH

---

### Headers

Examples:

- X-Original-URL
- X-Rewrite-URL

---

### Parameters

- Query Parameters
- JSON Body
- Form Data
- Cookies

Always ask:

> Can the server be tricked into making a different authorization decision?

---

## Step 5 - Analyze the Response

Don't rely only on the status code.

Inspect:

- Response Body
- Headers
- Redirects
- Response Length
- Returned Data

Some vulnerabilities are blind.

A request may return:

403 Forbidden

while the action was actually performed successfully.

Always verify the application's state after testing.

---

## Mentality

The objective is not simply to obtain a 200 OK response.

The objective is to determine whether the server made the correct authorization decision.

Always ask:

> Did the server allow something that should never have been allowed?

----
Choose Target

↓

Understand How It Works

↓

Understand How Authorization Works

↓

Identify Trust Points

↓

Challenge Those Trust Points

↓

Observe Response

↓

Confirm Impact

---

# Phase 4 - Validate, Expand & Explain

Finding an access control vulnerability is only the beginning.

The goal is to fully understand its impact and root cause.

---

## Step 1 - Validate

Confirm that the vulnerability is real.

Ask yourself:

- Was authorization actually bypassed?
- Was the action really performed?
- Was sensitive information actually disclosed?
- Is this simply a different response, or a real security issue?

Never trust status codes alone.

Always verify the application's state.

---

## Step 2 - Measure the Scope

Once confirmed, determine how widespread the issue is.

Ask yourself:

- Does this affect only one endpoint?
- Does the same pattern exist elsewhere?
- Can the same technique be reused?

Search for similar:

- APIs
- Profile pages
- Orders
- Billing
- Files
- Messages
- Administrative functions

One vulnerability often indicates an insecure design pattern.

---

## Step 3 - Chain the Vulnerability

Always think beyond the initial finding.

Ask:

What else becomes possible now?

Examples:

- Read another user's data
- Modify another user's account
- Change passwords
- Access administrative functionality
- Escalate from Horizontal to Vertical
- Reach sensitive internal features

The impact is often more valuable than the initial bug.

---

## Step 4 - Explain the Root Cause

Try to understand why the vulnerability exists.

Possible causes include:

- Missing authorization checks
- Authorization implemented in the wrong place
- Middleware not applied
- Platform misconfiguration
- Client-controlled identifiers
- HTTP method discrepancies
- URL matching discrepancies
- Trusting client-side data

Understanding the cause helps you discover similar vulnerabilities in the future.

---

## Step 5 - Document

Record:

- Target
- Expected behavior
- Actual behavior
- Exploitation steps
- Impact
- Root cause
- Lessons learned

Good documentation improves both reporting and future testing.



# Mental Model 

```text
          Understand

               │

               ▼

        Observe Carefully

               │

               ▼

      Build Hypotheses

               │

               ▼

      Choose One Target

               │

               ▼

 Understand Its Authorization

               │

               ▼

   Challenge Assumptions

               │

               ▼

 Validate the Finding

               │

               ▼

 Expand the Scope

               │

               ▼

 Explain the Root Cause
```
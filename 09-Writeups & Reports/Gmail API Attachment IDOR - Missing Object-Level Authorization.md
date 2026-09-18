# Case Study — Gmail API Attachment IDOR (Missing Object-Level Authorization)

> **Original write-up:** [Material Security — How Material Security Uncovered a Vulnerability in the Gmail API](https://material.security/resources/how-material-security-uncovered-a-vulnerability-in-the-gmail-api)
> **Target:** Gmail API (`users.messages.attachments.get`) — Google Workspace / public Gmail
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *ID-issuing endpoint enforces ownership* vs *ID-consuming endpoint trusts the ID alone*).

---

## TL;DR

`users.messages.get` correctly refused to hand out `attachmentId`s for messages you can't access — but `users.messages.attachments.get` accepted **any valid `attachmentId`** from **any authenticated Google user** and returned the attachment content, ignoring ownership entirely. The `messageId` parameter wasn't even validated (`"foo"` worked). Reported to Google's Bug Bounty (Jan 2023), fixed quickly. Blast radius was capped only because `attachmentId`s are long/unguessable — not by authorization.

---

## The Chain (foundation → application)

### 1) The two-step data-access pattern
Gmail attachments are fetched in two steps:

1. **Step 1 — enumerate (safe):** `users.messages.get` returns message metadata **including `attachmentId`s** — but never the raw file bytes.
2. **Step 2 — fetch (vulnerable):** `users.messages.attachments.get` takes the `attachmentId` and returns the content.

```
GET /gmail/v1/users/{userId}/messages/{messageId}
→ { ..., "attachmentId": "ANGjdJ8..." }

GET /gmail/v1/users/{userId}/messages/{messageId}/attachments/{attachmentId}
→ { "data": "<base64 attachment bytes>" }
```

> Step 1 enforced authorization correctly (no `attachmentId` for messages you can't see). Step 2 didn't. → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]

### 2) The anomaly that started it — IDs that never settle
While writing attachment-related code, Material engineers noticed: **every call to `users.messages.get` for the same message returned a *different* `attachmentId`** — and **all previously returned IDs stayed valid**.

> That means the backend keeps an ever-growing association table (`attachmentId` → attachment bytes) instead of a stable 1:1 mapping. A growing table of forever-valid bearer tokens with no ownership column is the smell to chase.

### 3) Hypothesis → permutation testing
If IDs are minted loosely, maybe they're *consumed* loosely too. They tested permutations of (`messageId`, `attachmentId`) against `attachments.get`:

1. Valid `messageId` + valid `attachmentId` from **someone else's mailbox** → **attachment content returned**. ✗
2. `messageId = "foo"` + valid `attachmentId` → **attachment content still returned**. ✗✗

> The `messageId` parameter was decorative — the endpoint resolved the attachment **by `attachmentId` alone** with no `attachment.owner == session.user` check.
> → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]] (Phase 3 — swap/drop each reference independently, including garbage values)

### 4) Exploit shape (minimal)
```http
GET /gmail/v1/users/me/messages/foo/attachments/ANGjdJ8_valid_id_of_victim HTTP/1.1
Host: gmail.googleapis.com
Authorization: Bearer <ATTACKER_OAUTH_TOKEN>
```
Response: `200 OK` + base64 attachment bytes — regardless of whose mailbox the attachment lives in.

> Authenticated (any Google account) ≠ authorized (owner of that attachment). Same AuthN/AuthZ split as every other case in this repo.

### 5) Why it didn't burn the internet — and where it still hurt
- **Capped:** `attachmentId`s are long/random → brute force impractical → no mass enumeration (compare: sequential `postId` 0→10M in the S3 report case).
- **Still dangerous:**
  1. Any org/app that **logged or stored `attachmentId`s** had to treat them as raw attachment data — same sensitivity.
  2. Any **third-party app** ever granted Gmail read access may have stored IDs; **revoking the app didn't revoke the IDs** (valid for 1+ year in testing, expiry only after the attachment itself is deleted).

### 6) The missing check
```python
# What the endpoint SHOULD do (pseudocode)
def get_attachment(request):
    att = lookup_by_attachment_id(request.attachment_id)
    msg = lookup_message(request.message_id)  # must exist + belong to caller

    # MISSING (both of these):
    if msg is None or msg.owner != request.user:
        return 404  # don't reveal existence
    if att.message_id != msg.id:
        return 404  # bind attachment to its message

    return att.data
```

Fix = bind the ID to its owner object on **every** read, and validate **all** references in the request (not just the longest one).

---

## Concept Mapping

- **Vulnerability class:** **BOLA / IDOR (horizontal)** — object reference (`attachmentId`) is the only guard, ownership never verified at read time.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Horizontal access controls|Horizontal access control]]
- **Root cause:** *auth ≠ authz* on the consuming endpoint. Step 1 (issuing) checked ownership; Step 2 (consuming) trusted the bearer ID.
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Sibling pattern in this repo:** same two-layer shape as [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]] — issuing endpoint vs consuming endpoint must *each* authorize; unguessable reference (`backgroundJobId` / `attachmentId`) ≠ permission.
- **Scope lesson:** unguessable IDs cap *enumeration* but never replace *authorization*; revocation must cover derived references (IDs), not just the original grant (OAuth token).

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"Unstable ID" as a discovery signal** — same object returning a *different* ID on every read (plus old IDs staying valid) means a backend association table is being built. Immediately test cross-owner + garbage-sibling-parameter permutations.
2. **Permute every reference independently** — for multi-parameter reads (`messageId` + `attachmentId`), swap each one separately *and* try garbage (`"foo"`, empty, deleted ID). A parameter the server ignores is itself the finding.
3. **Issuing-vs-consuming split** — when one endpoint mints a reference and another redeems it, test authorization on *both*. The minting side is often correct; the redeeming side is where the check is forgotten.
4. **Stored references inherit data sensitivity** — any logged/stored `attachmentId`, `jobId`, presigned path, or share token must be classified like the data it unlocks. Audit logs, caches, and third-party stores accordingly.
5. **Revocation must cover derived tokens** — deauthorizing an OAuth app / rotating a session is insufficient if derived bearer references (old `attachmentId`s) stay valid. Test: does revocation kill the derived ID too?

---

## Key Takeaways

1. **Unguessable ≠ authorized** — long random IDs stop enumeration, never authorization. Every read keyed by an ID still needs `owner == requester`.
2. **Validate *all* parameters, not the longest one** — `messageId` ignored + `attachmentId` trusted = the endpoint effectively takes one bearer token with no context.
3. **Test redeeming endpoints hardest** — minting endpoints get the security review; redeeming endpoints (`/attachments/{id}`, `/result/{jobId}`, `/download/{token}`) get forgotten. Start there.
4. **Garbage-value test is cheap and decisive** — `messageId=foo` returning `200 OK` proves non-validation in one request. Always include it in the IDOR matrix.
5. **Think in lifetimes** — non-expiring derived IDs (1+ year here) turn any past leak into a present breach. Expiry + revocation-binding are part of the fix, not extras.

---

## References

- [How Material Security Uncovered a Vulnerability in the Gmail API — Material Security](https://material.security/resources/how-material-security-uncovered-a-vulnerability-in-the-gmail-api)
- API docs: [`users.messages.get`](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get) / [`users.messages.attachments.get`](https://developers.google.com/gmail/api/reference/rest/v1/users.messages.attachments/get)
- Sibling case: [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

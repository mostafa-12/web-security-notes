# Case Study — From IDOR to Fraud (Travel Booking Platform, bookingId)

> **Original write-up:** [From IDOR to Fraud: Breaking Access Control in a Travel Booking Platform — Romene Mohtadi It (Medium)](https://medium.com/@romene.mohtadi.it/from-idor-to-fraud-breaking-access-control-in-a-travel-booking-platform-ef63f6b0bb2b)
> **Researcher:** Romene Mohtadi It — Published Sep 2026 (3 min read)
> **Target:** Anonymous production travel booking platform (`/fr/account/getbooking`, `/fr/account/getbookingFlight`)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *client supplies `bookingId`* vs *server trusts it without ownership check*).

---

## TL;DR

Two authenticated `GET` endpoints expose bookings by `bookingId` with **no object-level authorization**. Changing `bookingId=180845 → 180844` returns another user's PII (full name, email, phone, travel + ticket details). Sequential IDs = mass enumeration. The write-up claims a full `IDOR → fraud` chain (phishing, impersonation, ATO, refund abuse) but **proves only the read IDOR** — the fraud steps are theorized, not demonstrated.

---

## The Chain (foundation → application)

### 1) The feature — My Bookings

```
User (session) → /fr/account/getbooking?bookingId=XXXX → own booking JSON
User (session) → /fr/account/getbookingFlight?bookingId=XXXX → own flight JSON
```

Expected contract: `booking.owner == session.user`.

### 2) Standard flow (allowed)

Authenticated request intercepted (valid session):

```http
GET /fr/account/getbookingFlight?bookingId=180845 HTTP/1.1
Host: target.com
Cookie: session=<OWN_SESSION>
```

Response: own booking (name, email, phone, itinerary, ticket). Expected.

### 3) Exploit shape (minimal) — IDOR

Swap one digit:

```http
GET /fr/account/getbookingFlight?bookingId=180844 HTTP/1.1
Host: target.com
Cookie: session=<OWN_SESSION>
```

Result: `200 OK` + **another user's** full record:

```text
full name
email address
phone number
travel details
booking / ticket information
```

Same behavior on:

```http
GET /fr/account/getbooking?bookingId=180844 HTTP/1.1
```

> The check that should exist: `booking.owner_id == session.user_id` **before** returning the row. It's missing on both endpoints = systemic, not isolated.

### 4) Scaling — sequential IDs

`180845 → 180844` proves IDs are **sequential numeric**. So:

1. Send to Burp Intruder, payload on `bookingId`.
2. Range around known ID (± N).
3. Grep for `200 + email/phone` pattern.

> ⚠️ Scope note: don't dump the whole range on prod. Prove with 2 accounts (own A + own B), then state mass enumeration is possible.

### 5) Claimed vs proved impact

**Proved (read primitive):**

```text
Attacker (any authenticated user) → swap bookingId → victim PII + itinerary
```

**Claimed but NOT proved (write / fraud primitive):**

```text
❌ booking modification demonstrated
❌ refund abuse demonstrated
❌ account takeover demonstrated
❌ credential theft demonstrated
```

What IS realistic from the proved leak without extra bugs:

1. **Targeted phishing** with real booking context (flight date, PNR) — high success rate.
2. **Support impersonation** (name + email + phone + booking ref = passes weak KBA).
3. **Privacy / regulatory breach** (GDPR PII + travel movement).

What NEEDS an extra bug:

```text
ATO → needs password-reset / email-change / session flaw
Refund / modification fraud → needs missing authz on POST / PUT / cancel / refund endpoints
```

> Write the report as `proved: mass PII leak` + `possible: phishing → impersonation → fraud if write endpoints share the same missing check`. Don't present the chain as done.

### 6) The missing check

```python
# What the endpoint SHOULD do (pseudocode)
def getbookingFlight(request):
    user = get_user_from_session(request.session)
    booking = get_booking_by_id(request.query.bookingId)

    # MISSING:
    if booking.owner_id != user.id:
        return 403  # not your booking

    return booking.to_json()
```

Fix = per-request ownership check + centralized authz (RBAC/ABAC) + unpredictable IDs (UUID) + rate-limit + audit log on sensitive reads. UUID alone is NOT a fix.

---

## Concept Mapping

- **Vulnerability class (primary):** **BOLA / IDOR (horizontal, read)** — `bookingId` is the only guard, client-controlled, ownership never verified.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]] + [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Horizontal access controls|Horizontal access control]]
- **Root cause:** *auth ≠ authz* — endpoint validates session (AuthN) but skips `can_read(user, booking)` (AuthZ). Trust in client-controlled identifier.
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Enumeration pattern:** sequential IDs + Repeater → Intruder = single IDOR → mass exposure.
  → [[04-Recon/Discovering Hidden Content/Brute Force.md|Guided Brute Force]] + sibling [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]]
- **Sibling pattern in this repo:** same issuing-vs-consuming / read-vs-write split as [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]] (prove read, don't assume write), same `Origin/UI-hides` confusion as [[09-Writeups & Reports/Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]] (separate proved vs possible), same two-account diff as [[09-Writeups & Reports/Easy P3 Broken Access Control - Employee Profile Update]].
- **Overkill lesson:** title promises `IDOR → Fraud`, body proves `IDOR → PII`. Fraud needs a write primitive that was never shown.
  → Same `proved-vs-possible` rule as [[09-Writeups & Reports/Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)#Q&A (my questions to understand the report)]]

---

## Q&A (my questions to understand the report)

#### Q1 — Why is `180845 → 180844` enough to prove systemic issue?
One-off decrement succeeding on **two** endpoints (`getbooking` + `getbookingFlight`) with the same param name means the ownership check is missing in a shared layer / copy-pasted code, not a single typo. Both read paths trust `bookingId` alone.

#### Q2 — Does PII + itinerary alone justify Critical?
Yes for privacy/regulatory impact (names, emails, phones + travel movement = highly phishable + GDPR). No need to inflate to ATO/fraud to make it Critical — mass readable PII via sequential ID is already High/Critical.

#### Q3 — Why is the fraud chain "plausible but not proven"?
Phishing + support impersonation follow directly from leaked KBA fields (name, phone, PNR). ATO + refund abuse require **write** access (`POST /cancel`, `/refund`, `/change-email`) which was never tested. Read IDOR ≠ write IDOR until proven with a second PoC.

#### Q4 — What would have made this write-up non-overkill?
Same finding + (1) redacted response sample, (2) two-own-accounts PoC (A reads B, B reads A), (3) test of one write endpoint with the same swap, (4) explicit `proved vs possible` split. Title then becomes `Sequential bookingId IDOR Exposes All Travel Bookings`.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **`±1 decrement as first IDOR oracle`** — on any `?bookingId= / ?orderId= / ?id=` with numeric value, try `-1 / +1` before Intruder. Instant `200 + other user data` = fastest BOLA signal.
2. **Twin-endpoint check (`getbooking` vs `getbookingFlight`)** — same feature, two views (booking + flight). If one is IDOR, immediately test the sibling — shared backend = shared missing check.
3. **Travel-PNR as phishing amplifier** — itinerary fields (date, route, PNR, ticket) are stronger than generic PII for severity argument: attacker can craft `your flight X on date Y is cancelled, click here` with zero guesswork.
4. **Proved-vs-possible impact split** — write every IDOR report as `proved: ...` + `possible if write endpoints share the flaw: ...`. Prevents title overkill and survives triage pushback.

---

## Key Takeaways

1. **Never trust `bookingId` from the client** — every `GET` keyed by ID needs `owner == requester`, server-side, per request.
2. **Sequential IDs turn one IDOR into mass leak** — UUIDs raise enumeration cost but never replace authz.
3. **Two endpoints, same param = test both** — systemic BAC lives in shared code; one PoC is never enough.
4. **PII + itinerary is already Critical** — don't need to claim ATO/fraud to justify severity.
5. **Separate proved from possible** — phishing/impersonation = direct; ATO/refund = needs a second (write) PoC.
6. **Two own accounts = clean PoC** — A reads B's booking + B reads A's, no prod-user data touched.

---

## References

- [From IDOR to Fraud: Breaking Access Control in a Travel Booking Platform — Romene Mohtadi It (Medium)](https://medium.com/@romene.mohtadi.it/from-idor-to-fraud-breaking-access-control-in-a-travel-booking-platform-ef63f6b0bb2b)
- Sibling cases: [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]] + [[09-Writeups & Reports/Unauthenticated Payment Processing Endpoint - CWE-306 (CVSS 8.5)]] + [[09-Writeups & Reports/Easy P3 Broken Access Control - Employee Profile Update]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

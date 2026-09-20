# Case Study — Facebook Event Co-Host IDOR (Adding Anyone Including Blocked Users)

> **Original write-up:** [Adding anyone including non-friend and blocked people as co-host in personal event! — Bugreader](https://bugreader.com/binit@adding-anyone-including-non-friend-and-blocked-people-as-co-host-in-personal-event-181)
> **Researcher:** Binit Ghimire (binit) — Published 02 May 2020
> **Target:** Facebook Events Web (`/ajax/create/event/submit/`) — personal events
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *UI picker enforces Friends-only* vs *submit endpoint trusts `co_hosts[0]` alone*).

---

## TL;DR

Creating an event from a personal profile shows a **Co-hosts picker limited to friends**. The submit endpoint didn't enforce it: intercept the create request, replace the friend's ID in `co_hosts[0]=1008` with any victim ID (`co_hosts[0]=31337` — non-friend, non-friend-of-friend, or blocked in either direction), forward, and the victim lands in **pending co-host** + gets a notification *"User A made you a host of his/her event"*. Victim **could not reject**, and was shown as public co-host automatically. Reported 25 Nov 2019, reproduced Dec 2019, patched 21 Jan 2020, bounty **$750** on 24 Jan 2020. Severity: **MEDIUM, VALID**, inclusion in 2019 Thanks page.

---

## The Chain (foundation → application)

### 1) The feature — personal Event + Co-hosts

Personal event creation:

```
Host (User A) + Co-hosts[] (pending → accepted)
```

UI contract: Co-hosts field = searchable friend list only. No friend = not selectable.

### 2) The two access paths (secure vs vulnerable)

Same data, two enforcements:

1. **Via UI (safe):** friend picker → only `User B (friend, 1008)` selectable. ✓
2. **Direct submit (vulnerable):** `POST /ajax/create/event/submit/` takes `co_hosts[0]` as raw user ID, creates event with no friendship/block check. ✗

> Frontend hiding ≠ security: the picker is a suggestion, the ID is replayable directly against the API.

### 3) Exploit shape (minimal)

Setup: `User A (attacker, 1337)` + `User B (friend, 1008)` + `User C (victim, 31337, stranger)`.

Steps:
1. Login as User A → `facebook.com/events/` → Create Event (private or public).
2. Host = User A. Fill title/desc/location/dates normally.
3. Co-hosts = type `User B`, select him.
4. Start Intercept (Burp / ZAP) → click Create → forward until:

```http
POST /ajax/create/event/submit/?title=[EventName]&description=[Description]&location=...&co_hosts[0]=1008&start_date=11%2F25%2F2019&... HTTP/1.1
```

5. Swap:

```
co_hosts[0]=1008  →  co_hosts[0]=31337
```

6. Forward. Event created → open `1 co-host pending` → User C listed.
7. Login as User C → notification: *"User A made you a host of his/her event [EventName]."*

### 4) The exceptional case — block doesn't stop it

If User C blocked User A (or vice versa), the swap **still succeeds**. Only difference is visibility:

- Attacker side: User C still appears in pending co-host list.
- Victim side: User C can't open the event (block hides attacker's content), so no visible notification — but the forced association persists on the attacker's side.

> Block is a privacy boundary, not an authorization check on this endpoint. The endpoint never queried the block graph.

### 5) Why impact is higher than "just a notification"

From the timeline Q&A with Facebook Security Team:

1. **No reject path:** victim unable to reject the co-host invite.
2. **Auto-public:** victim automatically visible to the public as host of an event they never joined.
3. **Forced association + spam:** attacker can attach anyone (including people who blocked him) to abusive, political, or scam events.

Classic reputation / harassment primitive, not just UI annoyance.

### 6) The missing check

```python
# What the endpoint SHOULD do (pseudocode)
def create_event(request):
    host = request.user  # User A
    for co_host_id in request.getlist("co_hosts"):
        victim = lookup_user(co_host_id)

        # MISSING (all of these):
        if not are_friends(host, victim):
            return 400  # UI allows friends only — enforce it here
        if is_blocked(host, victim) or is_blocked(victim, host):
            return 400  # block in either direction = deny
        # + require explicit accept before public listing
        # + don't notify / list until accepted

    return create_event_row(host, co_hosts_pending)
```

Fix = enforce friendship + bidirectional block check on **every** write of `co_hosts[]`, and require opt-in before public attribution.

---

## Concept Mapping

- **Vulnerability class:** **IDOR / BOLA (write)** — `co_hosts[0]` is the only guard, relationship never verified at write time.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]
- **Root cause:** *client-side allowlist, no server-side authz* + missing block-graph check.
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Sibling pattern in this repo:** same UI-hides-but-backend-trusts shape as [[09-Writeups & Reports/From Internal User to Admin - Broken Access Control in SaaS]] (`companyUserRoles[]` replay) and [[09-Writeups & Reports/Easy P3 Broken Access Control - Employee Profile Update]] (read-only UI, writable API); same forced-association harm as [[09-Writeups & Reports/Facebook Analytics Private Chart Disclosure via IDOR]] (private promise broken by direct child endpoint).
- **Scope lesson:** sequential / known user IDs (Facebook profile IDs) = no entropy barrier — any ID is directly weaponizable, unlike unguessable `attachmentId` in the Gmail case.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"Friendly-ID swap"** — any picker limited to friends/members is a bypass candidate: pick a valid friend to satisfy the UI, then swap the ID to stranger/blocked in the intercepted request.
2. **Bidirectional block matrix** — test all four states: `attacker blocks victim`, `victim blocks attacker`, `mutual`, `none`. Backends often check one direction only — or neither, as here.
3. **Pending-state as proof** — `pending co-host / pending invite` listing on the attacker side is sufficient PoC even when the victim side is blind (blocked). Screenshot both sides.
4. **No-reject = severity upgrade** — always test: can the victim decline/remove themselves? Forced + public + irremovable turns a LOW annoyance into a MEDIUM harassment primitive. Ask it explicitly in the report (as Binit did).

---

## Key Takeaways

1. **Picker ≠ permission** — every friend-only dropdown must re-validate `friend(host, id)` server-side. Client allowlists are UX, not authz.
2. **Block graph is an authz input** — any endpoint that links two users must check `blocked(A,B) OR blocked(B,A)` before creating the link or sending a notification.
3. **Require opt-in before attribution** — never list someone publicly as host/member/admin while still `pending`. No-reject + auto-public = the real bug.
4. **Known IDs need no enumeration** — profile/user IDs are public, so a missing check here is immediately mass-exploitable. No Intruder needed.
5. **Prove both sides** — attacker view (pending list) + victim view (notification / profile attribution) + blocked-view (still listed) = complete PoC that survives triage pushback.

---

## References

- [Adding anyone including non-friend and blocked people as co-host in personal event! — Bugreader](https://bugreader.com/binit@adding-anyone-including-non-friend-and-blocked-people-as-co-host-in-personal-event-181)
- Sibling case: [[09-Writeups & Reports/From Internal User to Admin - Broken Access Control in SaaS]]
- Sibling case: [[09-Writeups & Reports/Easy P3 Broken Access Control - Employee Profile Update]]
- Sibling case: [[09-Writeups & Reports/Facebook Analytics Private Chart Disclosure via IDOR]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

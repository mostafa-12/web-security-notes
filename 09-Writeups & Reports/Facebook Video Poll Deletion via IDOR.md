# Case Study — Facebook Video Poll Deletion via IDOR

> **Original write-up:** [Deleting Anyone's Video Poll — Bugreader](https://bugreader.com/testgrounds@deleting-anyones-video-poll-175)
> **Researcher:** Dan Melamed (testgrounds) — Published 25 Apr 2020
> **Target:** Facebook Web (`/video/edit/dialog/save/`) — video polls on Pages
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *save endpoint enforces ownership on `VIDEO ID`* vs *delete handler trusts `deleted_poll_ids[0]` alone*).

---

## TL;DR

Facebook's new video-poll feature let Page owners attach a poll to a video. The edit-save endpoint checked you can edit your own `VIDEO ID` (`?v=(VIDEO ID)&av=(PAGE ID)`), but the `deleted_poll_ids[0]=(POLL ID)` parameter was never bound to that video. Swap your own `POLL ID` for a victim's `POLL ID` in the intercepted save request and the victim's poll is deleted. Reported 01 Nov 2018, reproduced + triaged 02 Nov 2018, fixed 06 Nov 2018, bounty awarded 06 Nov 2018. Severity: **MEDIUM, VALID**.

---

## The Chain (foundation → application)

### 1) The feature — Video + Polls

Video publishing flow on a Page:

```
Video (owner=Page) + Polls[] (attached to video)
```

Edit page has a Polls tab: create poll → submit video → poll goes live with the video.

### 2) The two access paths (secure vs vulnerable)

Same data, two checks:

1. **Via UI (safe):** you open *your* video → Edit → delete *your* poll → Save. You only ever see your own `POLL ID`. ✓
2. **Direct save (vulnerable):** `POST /video/edit/dialog/save/?v=(YOUR_VIDEO_ID)&av=(YOUR_PAGE_ID)` takes `deleted_poll_ids[0]` as a raw poll ID, deletes that poll row with no `poll.video_id == request.video_id` check. ✗

> Frontend scoping ≠ security: the edit page only shows your polls, but the ID is replayable directly against the API.

### 3) Exploit shape (minimal)

Setup: `Attacker Page + Attacker Video + Attacker Poll` + `Victim Video + Victim Poll`.

Steps:
1. Upload a video to your own Facebook Page.
2. In the video editing page → Polls tab → create a new poll → submit the video.
3. Go back and edit the video. Delete the poll, and before hitting Save, start Intercept (Burp / ZAP).
4. Capture:

```http
POST /video/edit/dialog/save/?v=(ATTACKER_VIDEO_ID)&av=(ATTACKER_PAGE_ID) HTTP/1.1
Host: www.facebook.com

...&deleted_poll_ids[0]=(ATTACKER_POLL_ID)&...
```

5. Swap:

```
deleted_poll_ids[0]=(ATTACKER_POLL_ID) → deleted_poll_ids[0]=(VICTIM_POLL_ID)
```

6. Forward. The victim's video poll is now deleted.

### 4) Why it happens

- **Wrong assumption:** "Save runs on my video, so any poll ID inside it must be mine." Forgets the attacker controls the body.
- **Parent validated, child not:** endpoint verifies `user can_edit(videoId)` but then does `delete_poll_by_id(pollId)` with no `poll.video_id == videoId` + no `poll.owner == request.user` check.
- **Array param blind spot:** `deleted_poll_ids[0]` looks like an internal bookkeeping field, so it skipped security review — exactly where IDOR lives.

### 5) The missing check

```python
# What the endpoint SHOULD do (pseudocode)
def save_video_edit(request):
    video = lookup_video(request.v)  # ?v=(VIDEO ID)
    if not user_can_edit(request.user, video, request.av):
        return 403

    for poll_id in request.getlist("deleted_poll_ids"):
        poll = lookup_poll_by_id(poll_id)

        # MISSING (both of these):
        if poll is None or poll.video_id != video.id:
            return 404  # don't reveal existence, don't delete
        if poll.owner != request.user and not user_can_edit(request.user, video):
            return 403

    return delete_polls_and_save(video)
```

Fix = bind every child ID to its parent object on **every** write, and validate **all** references in the request (not just `v` + `av`).

---

## Concept Mapping

- **Vulnerability class:** **BOLA / IDOR (write/delete)** — `deleted_poll_ids[0]` is the only guard, parent-child link never verified at write time.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]
- **Root cause:** *auth ≠ authz* on the consuming write + missing parent-child binding (`poll.video_id == video.id`).
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Sibling pattern in this repo:** same Parent→Child shape as [[09-Writeups & Reports/Gmail API Attachment IDOR - Missing Object-Level Authorization]] (`Message → Attachment` = `Video → Poll`) and [[09-Writeups & Reports/Facebook Analytics Private Chart Disclosure via IDOR]] (`Dashboard → Chart`); same array-param replay as [[09-Writeups & Reports/Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]] (`co_hosts[0]` = `deleted_poll_ids[0]`) and [[09-Writeups & Reports/From Internal User to Admin - Broken Access Control in SaaS]] (`companyUserRoles[]`).
- **Scope lesson:** requires victim `POLL ID` — caps scale vs sequential IDs, but any leaked/known poll ID is immediately deletable with zero privilege on the victim video.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"Delete-array swap"** — any `deleted_*_ids[]`, `removed_ids[]`, `delete_ids[]` param is an IDOR candidate: create your own object to satisfy the UI, intercept the delete-save, swap to victim child ID.
2. **New-feature first** — freshly shipped sub-features (Polls on video here) get the security review last. Hunt the new tab/checkbox/sub-option before the core flow.
3. **Parent-ID + child-ID independence test** — for multi-ID writes (`v` + `av` + `deleted_poll_ids[0]`), keep a valid parent you own and swap only the child to victim's. Valid parent + foreign child succeeding = the finding.

---

## Key Takeaways

1. **Validate *all* IDs, not just the parent** — `v` + `av` checked but `deleted_poll_ids[0]` trusted = one bearer token with no context.
2. **Child must be bound to parent on every write** — `poll.video_id == video.id` + `owner == requester` before delete. No inheritance by URL.
3. **Array params need per-element authz** — loop over `deleted_poll_ids[]` and authorize each element, not the request once.
4. **Create-to-delete scaffold** — you need your own valid parent + child to reach the vulnerable code path. Build it, intercept, then swap.
5. **Write-IDOR = impact even without read** — no data leaked, but deletion of anyone's poll = integrity break + harassment/spam primitive.

---

## References

- [Deleting Anyone's Video Poll — Bugreader](https://bugreader.com/testgrounds@deleting-anyones-video-poll-175)
- Sibling case: [[09-Writeups & Reports/Gmail API Attachment IDOR - Missing Object-Level Authorization]]
- Sibling case: [[09-Writeups & Reports/Facebook Analytics Private Chart Disclosure via IDOR]]
- Sibling case: [[09-Writeups & Reports/Facebook Event Co-Host IDOR - Adding Anyone Including Blocked Users]]
- Sibling case: [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

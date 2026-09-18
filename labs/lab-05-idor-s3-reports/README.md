# Lab-05 — IDOR + Public S3 Report Exposure

**Recreates:** `IDOR + Public S3 Report Exposure.md`
**Run:** `python app.py` → `http://127.0.0.1:8005`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.
**Accounts:** `X-User: alice` (owns posts 1-3) and `X-User: bob` (owns 4-6). Open both isolated (the Pwnfox idea).

## Scenario
Export works as an async job: request a report → get a `backgroundJobId` → poll for the result → receive a `downloadUrl` on S3. The email path is bound server-side (looks safe), but the PDF path never checks ownership, and the bucket is public.

## Your goal
As `alice`, read a private report belonging to `bob` and reach the flag. Then try enumeration without any job ID.

## Starting points
- `POST /api/reports/generate` with `{"postId": 1}` and see the response.
- `GET /api/reports/result/<jobId>`.

## Success criteria
- Download a PDF report you don't own + `FLAG{...}`.
- `GET /s3-bucket/` lists all files (ListBucket).

## Hints
<details><summary>Hint 1</summary>Swap postId to a number you don't own in Repeater. Ownership is never checked.</details>
<details><summary>Hint 2</summary>UUIDs can't be guessed — but postId is sequential. The sequential ID is what you enumerate.</details>
<details><summary>Hint 3</summary>Open the downloadUrl with no auth headers at all. Then try ?list-type=2 on the bucket.</details>

Scope note: prove it on 2-3 IDs only. The original writeup swept to 10M — never do that outside this lab.
Solution in `SOLUTION.md`.

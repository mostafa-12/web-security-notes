# Juice Shop — BAC and Related Challenges Only

> Filtered from the general roadmap, focused on your current track: Access Control / IDOR.
> Sorted from **easiest to hardest** for effective learning (reversed vs the previous file).
> Each challenge: goal only — no solution.

## BAC Quick Primer (to link with your notes)

| Type | Core idea | Example in Juice Shop |
|------|-----------|----------------------|
| Vertical BAC | Normal user reaches admin-only functionality | `Admin Section` |
| Horizontal BAC / IDOR | User reads or modifies another user's object | `View Basket`, `Manipulate Basket` |
| Function-Level BAC | Sensitive function (delete/update) not properly restricted | `Five-Star Feedback`, `Product Tampering` |
| Object-Level / BOLA in API | Tampering with IDs inside API requests | `Forged Feedback`, `Forged Review` |
| CSRF | Forcing a victim to execute an unwanted action | `CSRF` |

Your repo references:
- `03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/`
- `03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md`
- `03-Web-Vulnerabilities/Access control vulnerabilities/Access Control Testing Methodology.md`
- `labs/lab-05-idor-s3-reports/` and `lab-10-vestaboard-idor/`

---

## Level 1: Foundations (⭐ - ⭐⭐)

### 1. View Basket — Horizontal / IDOR (⭐⭐) — [x] Done
**Goal:** View another user's shopping basket instead of your own.
**Concept it reinforces:** Object IDs passed in URL/API can be enumerated and swapped.

### 2. Admin Section — Vertical BAC (⭐⭐) — [ ] In progress
**Goal:** Reach the administration section blocked for regular users.
**Concept it reinforces:** Authentication (who you are) vs Authorization (what you are allowed to see). You already dumped JWTs for `customer` vs `deluxe` — compare them.

### 3. Five-Star Feedback — Function-Level BAC (⭐⭐)
**Goal:** Delete another user's feedback while you are neither its owner nor an admin.
**Concept it reinforces:** Who is allowed to call the delete function, and how does the server verify it?

### 4. Web3 Sandbox — Broken Access Control (⭐)
**Goal:** Interact with the Web3 sandbox and understand its boundaries.
**Concept it reinforces:** Light warm-up on isolation and access scope before heavier challenges.

## Level 2: BAC in the API (⭐⭐⭐)

### 5. Forged Feedback — BOLA / Object-Level (⭐⭐⭐)
**Goal:** Submit feedback impersonating another user without being that user.
**Concept it reinforces:** A `userId` sent in an API request can be forged if the server does not bind it to your session.

### 6. Forged Review — BOLA / Object-Level (⭐⭐⭐)
**Goal:** Publish or modify a product review as another user.
**Concept it reinforces:** Same idea as above, but on reviews. Compare both cases in your notes.

### 7. Manipulate Basket — Horizontal + Write (⭐⭐⭐)
**Goal:** Modify another user's basket contents (add/remove items).
**Concept it reinforces:** Next step after `View Basket`: that was Read-IDOR, this is Write-IDOR which is more impactful.

### 8. Product Tampering — Function-Level on Products (⭐⭐⭐)
**Goal:** Modify store product data as a regular user.
**Concept it reinforces:** The product API should be read-only for normal users — what happens if the update function is exposed?

### 9. CSRF — Session Riding (⭐⭐⭐)
**Goal:** Make a logged-in user execute an action unknowingly via a link or image.
**Concept it reinforces:** Important BAC derivative: the server trusts cookies too much and never verifies real user intent.

## Stretch Goal (optional, after the above)

### 10. Easter Egg Level One — Hidden Functionality (⭐⭐⭐⭐)
**Goal:** Reach a page/functionality completely hidden from the normal UI.
**Concept it reinforces:** Hidden endpoints and security by obscurity. Leave it for last.

---

## Suggested Solving Order
```
1 View Basket (done) -> 2 Admin Section -> 3 Five-Star -> 4 Web3 Sandbox
-> 5 Forged Feedback -> 6 Forged Review -> 7 Manipulate Basket
-> 8 Product Tampering -> 9 CSRF -> 10 Easter Egg
```

## Documentation Rule Per Challenge
For each challenge create a file like `00-View Basket.md` containing:
1. The original request
2. What you changed (different ID / different role / different function)
3. Server response before and after
4. Classification: Vertical vs Horizontal vs Function-Level vs BOLA

Start with #2 (`Admin Section`) since you already have its data open.

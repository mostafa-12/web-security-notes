# Case Study — Live Share Accept Bypass: Regular User Bypasses Admin Approval ($250)

> **Original write-up:** [Medium — Tonmoy Datta](https://medium.com/@tonmoydatta495/how-i-got-regular-users-to-bypass-admin-approval-and-accept-live-shares-broken-access-control-c4e086da86ec)
> **Target:** Anonymous SaaS platform (`redacted.com` — network/app synthetic testing + cross-org live-share)
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *UI/docs say Admin-only accept* vs *backend accept endpoint enforces no role check*).

---

## TL;DR

Accepting an **inbound live share** was supposed to be locked to **Org Admin / Account Admin** only. A plain **regular user** who received the invite email could click **Accept Invitation** and it just worked — no `403`, no "ask your admin", no disabled button. Once accepted, the external live test feed became visible **org-wide** in the receiver org (admins + regular users), with zero admin approval. Reported Nov 25 2025 → triaged Jan 12 2026 → rewarded **$250 / 5 pts (P4)** Jan 13 2026.

---

## The Chain (foundation → application)

### 1) The false assumption to attack

The permission gate existed **on paper / in UI for other flows**, but not on the actual accept path:

- Intended: only Org Admin / Account Admin can accept inbound live share; everyone else sees it only after admin approval.
- Actual: any regular user with the invite link can accept directly, and that single action materializes the share org-wide.

**Foundation:** [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]] — hiding a button ≠ enforcing a restriction. Authorization must be server-side, per request, on the state-changing endpoint.

### 2) Setup — two orgs, two roles

Standard BAC scaffold, cross-org this time:

1. **Org A** — sender: create test → send live share invite to a user in Org B.
2. **Org B** — receiver: recipient is a **regular user**, not an admin (verified via Users and Roles page).

> This gives you both sides of the trust boundary (sender + receiver) — the minimum setup for any invite/accept matrix.
> → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]

### 3) Standard flow analysis

#### A. Intended flow (admin accept)

```text
Regular User
     │
     │ Accept Share
     X
   DENIED
```

```text
Org Admin
     │
     │ Accept Share
     ▼
  Accepted
     │
     ▼
Visible to Org
```

#### B. Actual flow (regular user accept)

```text
Regular User
     │
     │ Accept Share
     ▼
  Accepted
     │
     ▼
Visible to Entire Org
```

> The server accepted an **unauthorized state transition**: `Pending → Accepted` by an actor without the required role.

### 4) Vulnerability execution (bypass)

1. From Org A, create test → `Live Share → User in Org B`.
2. Confirm receiver role = `Regular User` (not Org Admin / Account Admin).
3. Regular user opens invitation email → clicks `Accept Invitation`.
4. Expected: `403 Forbidden` / "You need administrator approval".
5. Actual: `SUCCESS` — share visible org-wide in Org B:

```text
Regular User A
      │
      │ Accept
      ▼
    Share
      │
      ├── Admin B       → Can see
      ├── Regular B 1  → Can see
      ├── Regular B 2  → Can see
      └── Regular B 3  → Can see
```

PoC proof: short video + screenshot of Users and Roles page (role = Regular User) alongside successful accept — removes ambiguity at triage.

### 5) The missing check

```python
# What the endpoint SHOULD do (pseudocode)
def accept_live_share(request):
    user = get_user_from_token(request.auth_token)
    share = get_share(request.share_id)

    # MISSING: Authorization check
    if user.role not in ("Org Admin", "Account Admin"):
        return 403 Forbidden  # "Ask your administrator"

    share.status = "Accepted"
    share.visible_to_org(share.receiver_org)
```

Fix = single server-side role check on **every** accept call: `requester.role == Org Admin OR Account Admin` before materializing the share org-wide. UI hiding elsewhere is not a substitute.

---

## Concept Mapping

- **Vulnerability class:** **Broken Access Control — vertical privilege escalation via workflow (not exploit code).** Regular user performs Admin-only state transition.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/Basic Concepts/Access Control Types.md#Vertical access control|Access Control Types]]
- **Root cause:** Missing server-side authorization on accept endpoint — security-through-UI-hiding / workflow assumption that only admins reach the endpoint.
  → [[07-CheatSheets/Input-Validation.md#Client-Side vs Server-Side|Client-Side vs Server-Side]]
- **Testing methodology:**
  1. Two orgs + two roles from the start
  2. Map role × function matrix (Observe)
  3. Test both sides of invite/accept (Hypothesize)
  4. Accept with low-priv user via real reachable path — email link (Test) → verify org-wide visibility (Validate)
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Multi-step context:** Invite → Pending → Accepted spans two orgs. Both sides of the handshake need the same scrutiny.
  → [[03-Web-Vulnerabilities/Multi-Step Processes.md|Multi-Step Processes]]

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **Accept-side audit for two-party workflows** — teams harden `Invite/Send` and forget `Accept/Approve`. For every `Invite → Accept/Reject/Cancel/Revoke`, test authorization on each action independently.
2. **Email-link as the bypass path** — even if UI hides Accept for regular users, the email link is a first-class entry point to the same endpoint. Always follow it with a low-priv session.
3. **State-transition framing for BAC** — don't just ask "can I see object X?"; ask "can I move object X from `Pending` → `Accepted/Approved/Published` without the required role?" States to hunt: `Pending, Approved, Rejected, Active, Disabled, Verified, Published, Accepted, Revoked`.
4. **Org-wide blast radius as severity lever** — one low-priv accept → share visible to entire org. Impact is not "I can see it" but "I forced it on everyone". Screenshot both the role proof and the org-wide result.
5. **Prove the boundary before the exploit** — report pattern: `Who am I? → What role? → What should I be unable to do? → What did I do? → What changed?` Kills triage back-and-forth.

---

## Key Takeaways

1. **Check both sides of any invite/accept flow** — RBAC bugs hide in the receiving half.
2. **Hidden button ≠ access control** — if the server doesn't check `role` on the accept endpoint, the path is open via email link / direct request / API.
3. **Think in state transitions, not just IDs** — IDOR is `change the ID`; this is `change the state without permission`. Both are BAC.
4. **Two orgs + low-priv user from minute one** — cross-org sharing features are RBAC gold mines; set up A (sender) and B (receiver, regular user) early.
5. **Patience pays in triage** — 7 weeks here including holiday gap + setup walkthrough request. Polite follow-ups with screenshots unblock faster than assuming it died.

---

## شرح مفصّل بالعربي (نفس الـ pattern خطوة بخطوة)

## How I Stumbled Onto It — إزاي اكتشف الثغرة؟

كان الباحث بيعمل **RBAC mapping** للتطبيق؛ يعني كان بيحاول يعرف، Role by Role، إيه اللي يقدر المستخدم العادي يعمله وإيه اللي محجوز للـ **Org Admin / Account Admin**.

وكان مهتم بشكل خاص بميزات **Sharing وInvitations**.

ليه؟

لأن الـ workflows دي غالبًا بتعمل **State Transition** وبتربط بين مستخدمين أو مؤسستين مختلفتين:

```text
Invited
   ↓
Pending
   ↓
Accepted
```

وهنا لاحظ نقطة مهمة جدًا:

لما يكون عندك workflow بين **Organization A** و **Organization B**، لازم تختبر طرفي العملية، مش الطرف اللي بدأ العملية فقط.

يعني ماينفعش تفترض:

```text
Sender side → protected
              ↓
        Receiver side → protected
```

ممكن جدًا الـ developers يكونوا عملوا authorization كويس عند إنشاء وإرسال الـ invitation، لكن نسوا يطبقوه عند **Accept**.

وده تقريبًا اللي حصل هنا.

### الـ Mental Model

بدل ما تسأل فقط:

> "هل الـ Regular User يقدر يعمل Invite؟"

اسأل:

> "هل الـ Regular User يقدر يكمل أي خطوة لاحقة في الـ workflow المفروض تكون Admin-only؟"

وده فرق مهم جدًا في اختبار الـ BAC.

---

# The Actual Bug — الثغرة نفسها

كان فيه Permission Gate من المفترض إنه يمنع الـ Regular User.

لكن الحماية كانت موجودة **على مستوى الـ UI / بعض الـ flows فقط**، وليست enforced فعليًا عند عملية الـ Accept.

الباحث عمل الآتي:

```text
Organization A
      │
      │ Live Share Invitation
      ▼
Organization B
      │
      ▼
Regular User
```

المستخدم في Organization B كان **Regular User وليس Admin**.

وصلته دعوة الـ Live Share في الإيميل، وكان فيها:

```text
Accept Invitation
```

ضغط عليها...

والعملية نجحت.

لم يحدث:

```text
"Ask your administrator"
```

ولم يتم تعطيل الزر.

والأهم:

**لم يكن هناك Server-Side Authorization Check يمنع العملية.**

وبمجرد قبول الـ share، أصبح الـ Live Share ظاهرًا لكل أعضاء Organization B، بما فيهم الـ Regular Users الآخرين.

---

# هنا بالضبط الـ BAC

السلوك المفروض:

```text
Regular User
     │
     │ Accept Share
     X
   DENIED
```

بينما:

```text
Org Admin
     │
     │ Accept Share
     ▼
  Accepted
     │
     ▼
Visible to Org
```

لكن الواقع:

```text
Regular User
     │
     │ Accept Share
     ▼
  Accepted
     │
     ▼
Visible to Entire Org
```

إذن المشكلة ليست مجرد أن زرًا ظهر لمستخدم غلط.

المشكلة الحقيقية هي أن:

> **Server accepted an unauthorized state transition.**

أي أن مستخدمًا لا يمتلك الـ role المطلوب استطاع نقل الـ Live Share من:

```text
Pending
```

إلى:

```text
Accepted
```

وهو Action كان المفروض يكون Admin-only.

---

# Steps to Reproduce — خطوات إعادة الإنتاج

## 1. من Organization A

أنشئ Test ثم أرسل **Live Share invitation** إلى مستخدم موجود في Organization B.

```text
Org A
  │
  └── Create Test
          │
          └── Live Share → User in Org B
```

---

## 2. تأكد أن المستلم Regular User

دي خطوة مهمة جدًا.

لازم الحساب الموجود في Organization B يكون:

```text
Role = Regular User
```

وليس:

```text
Org Admin
Account Admin
```

ليه؟

لأنك لو اختبرت باستخدام Admin، فلن تثبت وجود مشكلة في الـ authorization.

أنت تريد إثبات:

```text
User WITHOUT permission
            ↓
       performs action
            ↓
        SUCCESS
```

---

## 3. المستخدم العادي يفتح الـ invitation

الـ Regular User يستلم الإيميل ويدخل على:

```text
Accept Invitation
```

ويضغط Accept.

المفترض هنا أن السيرفر يقول:

```text
403 Forbidden
```

أو على الأقل:

```text
You need administrator approval
```

لكن في الحالة دي:

```text
Accept
  ↓
SUCCESS
```

---

## 4. النتيجة

بعد الـ Accept، أصبح الـ Live Share متاحًا على مستوى Organization B بالكامل.

يعني:

```text
Regular User A
      │
      │ Accept
      ▼
    Share
      │
      ├── Admin B       → Can see
      ├── Regular B 1  → Can see
      ├── Regular B 2  → Can see
      └── Regular B 3  → Can see
```

وبالتالي المستخدم العادي لم يحصل فقط على صلاحية لنفسه.

بل قام بعملية أدت إلى **تغيير حالة resource بحيث أصبح متاحًا للـ organization كلها**.

وده هو الجزء اللي بيرفع أهمية الـ finding.

---

# ليه الباحث أثبت الـ Role في الـ PoC؟

الباحث لم يكتفِ بأنه يقول:

> "أنا قدرت أعمل Accept."

هو أرفق:

- فيديو قصير للـ PoC
- Screenshot يوضح Role الحساب
- Screenshot/دليل على نجاح عملية الـ Accept

وكان الهدف إزالة أي ambiguity أثناء الـ triage.

يعني الـ triager يقدر يشوف:

```text
Account Role = Regular User
            +
Accept succeeded
            +
Share became available
```

وبالتالي الـ privilege boundary واضح جدًا.

دي نقطة مهمة لك في كتابة الـ reports:

**أثبت الـ authorization boundary قبل ما تثبت الـ exploit.**

يعني:

```text
Who am I?
      ↓
What role do I have?
      ↓
What am I supposed to be unable to do?
      ↓
What did I actually do?
      ↓
What changed?
```

---

# Why This Actually Matters — ليه الثغرة لها Impact؟

## 1. Privilege Escalation via Workflow

المستخدم لم يحتاج:

- exploit معقد
- bypass غريب
- code execution
- تغيير عشرات الـ parameters

هو فقط استخدم **Normal Feature Flow**.

لكن الـ workflow نفسه لم يطبق الـ authorization الصحيح.

يعني:

```text
Normal Feature
     +
Missing Authorization
     =
Broken Access Control
```

وده شكل شائع جدًا في الـ BAC.

الفكرة ليست أن "الباب مفتوح".

الفكرة أن:

> **الباب بيفتح لأي شخص لأن النظام لم يتحقق أصلًا من هو الشخص الذي يحاول الدخول.**

---

# 2. Data Integrity / Governance

المشكلة مش بس إن Regular User قدر يشوف الـ share.

هو أصبح قادرًا على **إدخال Live External Test Data إلى Organization** بدون موافقة Admin.

يعني الـ organization فقدت الـ control المفروض يكون عندها على:

```text
External Data
      ↓
Approval
      ↓
Organization
```

وأصبح:

```text
External Data
      ↓
Regular User
      ↓
Organization
```

وده يخالف الـ permission model اللي التطبيق نفسه مصممه.

---

# 3. Compliance Exposure

الكاتب أشار أيضًا إلى أن هذا النوع من الـ authorization gap يمكن أن يكون مشكلة للمنظمات التي تعتمد على سياسات access control أو متطلبات تدقيق مثل **SOC 2**.

النقطة هنا ليست أن الثغرة "تسبب SOC 2 failure تلقائيًا"، وإنما أن وجود فرق بين:

```text
Documented Permission Model
```

و:

```text
Actual Enforcement
```

يمكن أن يمثل مشكلة في عمليات الـ audit والـ governance.

---

# The Fix — إزاي المفروض تتصلح؟

الحل الأساسي:

**الـ server نفسه لازم يتحقق من الـ role قبل تنفيذ Accept.**

يعني عند وصول request:

```http
POST /some/accept-endpoint
```

السيرفر لازم يعمل conceptually:

```text
Who is making this request?
        ↓
What is their role?
        ↓
Are they Org Admin / Account Admin?
        ↓
       YES
        ↓
Accept Share
```

أما:

```text
Regular User
     ↓
Accept Share
     ↓
   DENIED
```

المهم هنا:

> **إخفاء الزر في الـ frontend ليس authorization.**

حتى لو الـ UI قال:

```text
Regular User → لا تعرض Accept
```

ده لا يكفي.

لأن المستخدم ممكن يصل إلى الـ action من:

- email link
- direct endpoint
- existing workflow
- API request
- old UI
- hidden functionality

لذلك الـ authorization الحقيقي يجب أن يكون **server-side** عند الـ sensitive action نفسها.

---

# Timeline — الـ Timeline

- **25 نوفمبر 2025:** تم إرسال التقرير.
- **ديسمبر 2025:** البرنامج طلب معلومات إضافية وتم تقديم التوضيحات.
- **8 يناير 2026:** البرنامج طلب شرحًا لكيفية إنشاء الـ test من البداية، وتم إرسال خطوات مع screenshots.
- **13 يناير 2026 (تصحيح: triaged 12 يناير):** تم تأكيد أن المشكلة قابلة لإعادة الإنتاج وتم عمل triage لها.
- **13 يناير 2026:** حصل الباحث على **$250 / 5 points** وتم اعتبار المشكلة resolved من جانب الباحث.

---

# أهم Takeaways بالنسبة لك

## 1. اختبر طرفي الـ workflow

لو عندك:

```text
Invite → Accept
```

لا تختبر:

```text
Invite
```

فقط.

اختبر:

```text
Invite
Accept
Reject
Cancel
Revoke
```

كل Action ممكن يكون له authorization مختلف.

---

## 2. Hidden Button ≠ Access Control

دي من أهم الجمل في التقرير:

```text
Hidden button ≠ authorization
```

لو الـ UI مش بيعرض:

```text
Accept
```

لـ Regular User، ده لا يعني أن الـ endpoint نفسه محمي.

أنت كـ tester تريد أن تعرف:

```text
Can the SERVER distinguish:


Admin
  vs
Regular User
```

عند تنفيذ الـ sensitive action؟

---

## 3. ركز على State Transitions

ودي أهم حاجة أعتقد أنك تستفيد منها في مرحلة الـ BAC الحالية.

لما تشوف:

```text
Pending
Approved
Rejected
Active
Disabled
Verified
Published
Accepted
Revoked
```

فكر فورًا:

> **مين مسموح له ينقل الـ object من State إلى State؟**

مثلاً:

```text
Pending
   │
   ├── Admin → Approved ✅
   │
   └── Regular User → Approved ❌
```

اختبارك هنا ليس فقط:

> "هل أقدر أشوف الـ object؟"

لكن:

> **"هل أقدر أغير حالته بطريقة لا أملك صلاحيتها؟"**

وده يوسع مفهوم BAC عندك جدًا.

---

# الـ Pattern اللي أريدك تحفظه من الـ Writeup

بدل ما تحفظ الـ endpoint أو الـ parameter، احفظ الـ pattern:

```text
Two Organizations
       ↓
Sharing / Invitation
       ↓
State Transition
       ↓
Admin-only Action
       ↓
Regular User
       ↓
Accept
       ↓
Server fails to enforce RBAC
       ↓
State changes
       ↓
Impact spreads to Organization
```

أو بشكل أبسط:

```text
        "Who can ACCEPT?"
                 ↓
        Don't trust the UI
                 ↓
       Test with low-priv user
                 ↓
       Does server check role?
                 ↓
             NO ❌
                 ↓
     Unauthorized state change
                 ↓
          Broader impact
```

**وده بالضبط النوع اللي أنت محتاج تبدأ تدور عليه في الـ Access Control بدل ما تحصر نفسك في IDOR وتغيير الـ IDs فقط.**

---

## References

- [How I Got Regular Users to Bypass Admin Approval and Accept Live Shares (Broken Access Control) — $250 Bounty — Tonmoydatta (Medium)](https://medium.com/@tonmoydatta495/how-i-got-regular-users-to-bypass-admin-approval-and-accept-live-shares-broken-access-control-c4e086da86ec)
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]
- Access Control Testing Methodology: [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md]]
- Multi-Step Processes (async / two-party): [[03-Web-Vulnerabilities/Multi-Step Processes.md]]

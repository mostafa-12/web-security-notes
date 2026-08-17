# Web Caching

> وكيف تتحول الـ Caching من ميزة أداء إلى ثغرة أمنية.

---

## 1) What is Caching?

حفظ الـ response ليعاد استخدامه لاحقاً — بدون تكرار الرحلة للـ backend.

طبقات الكاش:

```text
Browser Cache
    │
    ▼
CDN / Reverse Proxy (Nginx, Varnish, Cloudflare)
    │
    ▼
Application-level Cache (Redis, Memcached)
    │
    ▼
DB Query Cache
```

---

## 2) Cache-Control — أهم الـ Headers

| Directive | Meaning |
|-----------|---------|
| `Cache-Control: private` | فقط متصفح المستخدم يخزنها — **لا يوجد proxy يخزنها** |
| `Cache-Control: public` | أي proxy يستطيع تخزينها |
| `Cache-Control: no-store` | لا تخزين إطلاقاً |
| `Cache-Control: max-age=N` | تخزين لمدة N ثانية |
| `Cache-Control: no-cache` | يخزن لكن يجب إعادة التحقق قبل الاستخدام |
| `Pragma: no-cache` | HTTP/1.0 — توافق قديم |

> **الأهم للثغرات:** لو الـ response بيحتوي بيانات خاصة ويحمل `public` أو بدون `private`، فهو مرشح لأن يخدم لمستخدمين آخرين.

---

## 3) Cache Key — الحدود الأمنية للكاش

الكاش يخزن الـ response تحت **مفتاح** (Cache Key). عادةً:

```text
Cache Key = Method + URL + Query Parameters
```

المفتاح **لا يشمل الـ Authorization / Cookies / Headers** افتراضياً — إلا إذا أضافها المسؤول.

### القاعدة الذهبية:

> **لو الـ response يتغير حسب المستخدم (user-specific)، فإما لا تخزنه، أو أضف الـ auth context داخل الـ Cache Key.**

وإلا: response يخص admin سيُقدَّم لأي مستخدم يطلب نفس الـ URL في نفس نافذة الـ TTL.

```text
// خطأ أمني
Cache Key:  GET /graphql?op=GetOrders&shop_id=123
Response:   orders الخاصة بـ shop 123 (للأدمن فقط)

// أي مستخدم يطلب نفس المفتاح → يستلم بيانات الأدمن
```

---

## 4) Micro-Caching / Short-TTL

خزن لفترة قصيرة جداً (ثواني) لامتصاص الـ spikes وتخفيف الحمل عن الداتابيز.

- أول request يضرب الـ DB، والباقي في نفس النافذة ياخد الـ cached copy.
- شائع في الـ dashboards و GraphQL endpoints.

> **هذا ليس خطأ بذاته** — الخطأ هو خزن response خاص بالمستخدم تحت مفتاح عام.

---

## 5) ثلاث فئات من ثغرات الكاش

| Class                                           | Payload?                           | الفكرة                                                                                            |
| ----------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Web Cache Deception**                         | لا — مجرد طلب بـ `.css` أو `;`     | الـ cache يخزن response لصفحة خاصة لأن عنوانها يبدو عاماً، ثم يُقدَّم للجميع                      |
| **Web Cache Poisoning**                         | نعم — حقن في الـ key أو الـ header | المهاجم يجعل الكاش يخزن محتوى خبيث/خاص ثم يقدمه للضحايا                                           |
| **Cached Authorized Data → Unauthorized Users** | لا                                 | الـ backend يعرض بيانات الأدمن، الكاش يخزنها تحت مفتاح عام، وأي مستخدم يلتقطها داخل نافذة الـ TTL |

> الريبورت بتاع [Cache Misconfiguration](https://rikeshbaniya.medium.com/authorization-bypass-due-to-cache-misconfiguration-fde8b2332d2d) هو الفئة الثالثة: لا Deception ولا Poisoning — تخزين بسيط لبيانات خاصة بمفتاح عام.

---

## 6) Core Principle

نفس المبدأ في [[03-Web-Vulnerabilities/temp.md]]:

> مكونان يفسران نفس البيانات بشكل مختلف.

- **الـ cache** يفسر الـ request كأنه عام (URL فقط).
- **الـ backend** يفسره كأنه خاص (يحتاج admin token).
- النتيجة: Authorization Bypass من غير أي payload.

---

## 7) How to Test

1. **Autorize كـ cache oracle** — الـ replay الفوري للمستخدم العادي يقع داخل نافذة الكاش، فتراه "bypassed" بينما Repeater اليدوي يعطي 403.
   > **تناقض الأدوات = إشارة، ليس glitch.**
2. **فرق التوقيت** — نفس الـ request بتوكين admin ثم فوراً بتوكين user: لو الثاني جاب بيانات الأول → كاش خاص بالمستخدم.
3. **جرّب `Cache-Control` في الـ response** — لو sensitive pages بترجع `public` أو بدون `private` → مشبوهة.
4. **الـ race** — Script يرسل requests متتالية على نفس الـ URL أثناء فتح الأدمن للصفحة.

---

## 8) Mental Model (احفظها)

```text
1. هل الـ response بيختلف حسب المستخدم؟  → لو لأ، الكاش آمن
2. لو بيختلف: هل الـ Cache Key فيه الـ auth؟  → لو لأ → ثغرة
3. هل فيه نافذة TTL قصيرة؟  → نافذة استغلال
4. هل الـ ID المستخدم (shop_id) عام وقابل للتخمين؟  → يصعّد الأثر
```

---

## 9) Takeaway

> Rate limiting ليس إصلاحاً جذرياً — polling منخفض التواتر لن يُكتشف.
> الإصلاح الوحيد: الـ Cache Key يجب أن يتضمن الـ auth context، أو لا تخزن responses خاصة بالمستخدم أصلاً.
# Amazon S3

> خدمة **object storage** من AWS — بتخزن ملفات (objects) في حاويات اسمها **buckets**، وكل ملف ليه **key** (المسار جوه الـ bucket). أشهر استخداماتها في الويب: استضافة الملفات الثابتة والـ assets، **وتخزين الملفات المولّدة زي الـ PDFs والتقارير**.

## بنية بسيطة

```
https://s3.amazonaws.com/<bucket-name>/<key>
           ↑ storage domain        ↑        ↑ المسار/اسم الملف
```

الـ key = المسار الكامل للـ object. أي حد **عرف المسار** يقدر يطلبه — السؤال الوحيد: هل الـ bucket بيسمح بالقراءة العامة ولا لأ؟

## إزاي بيتحكم في الوصول (3 أنظمة بتشتغل مع بعض)

1. **Bucket Policy:** سياسة JSON (resource policy) على الـ bucket نفسه — بتقول مين يقدر يعمل إيه (Read، List، Write...) ومين ممنوع. أكتر حاجة بتظهر في الثغرات.
2. **IAM:** صلاحيات للمستخدمين/الأدوار جوه حساب AWS (بيطبق على الناس مش على الـ bucket).
3. **ACLs:** النظام القديم — AWS بترشّح الـ Bucket Policy بداله.

وبيضاف عليهم إعداد مهم:

- **Block Public Access (BPA):** مفتاح إيقاف لأي إعداد عام — من **2023** بيتفعّل **افتراضيًا** لأي bucket جديد. الـ buckets القديمة أو اللي حد عطّل فيه الإعداد ده هي اللي بتفضل معرّضة.

## مستويين مختلفين من التعريض (الأهم في الباونتيز)

### 1) Objects public-read (القراءة بالمسار بس)
```http
GET https://s3.amazonaws.com/companyname/report/20241013/{uuid}.pdf
```
أي حد **عرف الـ key** (المسار) ينزّل الملف — من غير أي login. دي الحالة اللي ظهرت في ريبورت الـ IDOR/Report Export. المشكلة هنا: محتاج تعرف الـ key من مكان تاني (الـ IDOR)، لأنك **مش قادر تعدّد** الملفات.

### 2) ListBucket عام (الـ enumeration) — الأسوأ
```http
GET https://s3.amazonaws.com/companyname?list-type=2
```
بيرجعلك **XML فيه كل الـ keys** (كل الملفات وجدولها) من غير ما تعرف أي UUID خالص. نفس الحاجة بالـ AWS CLI:

```
aws s3 ls s3://companyname/ --no-sign-request
aws s3api list-objects-v2 --bucket companyname --no-sign-request
```

> الـ `--no-sign-request` بيخلي الطلب anonymous. لو رجعلك الـ list → الـ bucket بيسمح بأي حد يعدّد كل الداتا → **Critical** حتى لو الـ API اللي فوقه سليم.

## ليه بيحصل في الحقيقة؟

- Buckets قديمة اتعملت في زمان ما كان التخزين public افتراضيًا.
- حد فكّ الـ BPA عشان يستضيف **static hosting** أو صور/ملفات عامة — ونسي إن جوه نفس الـ bucket ملفات **خاصة** (تقارير، فواتير، بيانات عملاء).
- فريق نزّل ملفات حساسة في نفس الـ bucket العام بتاع الـ CDN.
- **الدرس:** bucket واحد بيخدم "حاجتين" — عام وخاص — هو السبب الأكثر شيوعًا.

## ليه هو مهم في سياق Bug Bounty؟

- لو شفت `s3.amazonaws.com/<bucket>/...` أو `*.s3.amazonaws.com` أو `*.s3.region.amazonaws.com` في أي request أو JS bundle — ده **طبقة تخزين مستقلة** عن الـ API اللي ولّد الملف.
- بيجبلك سؤالين: (1) الملفات عامة بالمسار؟ (2) الـ bucket بيسمح بالـ list؟
- لو الملفات عامة، أي **تسريب للـ key** (من IDOR، logs، لينك متشارك، JS bundle) = وصول كامل.
- بيضاعف سيڤيريتي أي bug API تاني: الـ API لو متصلحش بـ ownership check، الـ bucket لسه ممكن يسرّب كل حاجة.

## إزاي تختبرها بمسؤولية في باونتي

1. افتح ملف من الـ bucket → لو رجّع الملف = objects عامة.
2. جرّب الـ list بدون sign (`?list-type=2` أو `--no-sign-request`) → لو رجع keys = ListBucket عام.
3. جرّب تجيب السياسة نفسها: `GET /?policy` → تشوف مين عامل إيه بالظبط.
4. **متجرّدش كل الداتا** — أثبت إن الـ list مفتوح بكام أمثلة، واكتب في الريبورت إن الـ enumeration الكامل ممكن. جرد كل بيانات الشركة بيبوظ الريبورت والـ scope.

## الفيكس الصح

- Bucket **private** (BPA شغّال).
- الوصول للملفات الحساسة عن طريق **Presigned URLs** — لينك فيه توقيع + وقت صلاحية قصير (دقايق)، مربوطة بالمستخدم اللي طلب الملف.
- تفصل الملفات العامة عن الخاصة في buckets مختلفة.

## فين بيظهر في الريبو

- الريبورت: `09-Writeups & Reports/IDOR + Public S3 Report Exposure.md`
- البنية الأساسية: `02-Web Architecture/Anatomy of a Web Request.md`

## References

- https://aws.amazon.com/s3/
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-overview.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
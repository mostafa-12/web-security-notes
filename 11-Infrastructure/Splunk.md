# Splunk

> أداة/منصة **log management & data analytics** — أشهر أدوات الـ **SIEM** في الشركات. مش أداة ويب بالمعنى الضيق، دي أداة back-end/infrastructure.

## وظيفته

بيجمع الـ logs والبيانات من كل مكان (سيرفرات، أجهزة، تطبيقات) ويخزنها في مكان واحد منظّم ويخليها قابلة للبحث والتحليل والتنبيه.

## بيعمل إيه بالظبط (4 مراحل)

1. **Ingestion (جمع البيانات):** التطبيقات/السيرفرات بتبعت الـ logs و الـ events لـ Splunk (كده اسمه Data Forwarding). الجهاز اللي بيبعت اسمه **Forwarder**.
2. **Indexing (فهرسة):** بيخزنها ويقسّمها على فهارس (indices) عشان البحث يبقى سريع.
3. **Search & Analysis (تحليل):** بلغة اسمها **SPL** (Search Processing Language) — تقدر تعمل queries على الـ logs زي SQL تقريبًا.
4. **Visualization & Alerts:** dashboards و تنبيهات — لو حصل سلوك شبه pattern معين، يعملك إشعار.

## مصطلحات مهمة (اللي بتيجي في الريبورتس)

| المصطلح | معناه |
|---------|-------|
| `instance` | عنوان الـ Splunk server اللي بيتبعت ليه البيانات (URL) |
| `index` | الـ data store اللي البيانات بتتحط فيه (البيانات بتتصنف فيه) |
| `token` | مفتاح الـ authentication اللي بيسمح بالتطبيق يبعت بيانات للـ instance |
| `source` | اسم/نوع مصدر البيانات اللي بتتبعت |

## ليه هو مهم في سياق Bug Bounty؟

- **التطبيقات بتوصّل البيانات ليه** (زي ما Sentry بيعمل forwarding للـ errors) — وإعدادات الربط دي (فين الأنسطنس + الـ token) ممكن تكون **ميزة مدفوعة** أو شغالة من غير رقابة (زي ريبورت ExamenTry).
- لو الأنسطنس بيتبعت ليه بيانات حساسة، الوصول غير المصرح بيه ليه = تسريب بيانات.
- بيفتح سؤال: مين يقدّر يعدّل إعدادات الربط (الـ forwarding)؟ لو أي حد عنده حساب فري — ده access control bug.

## فين بيظهر في الريبو

- التارجت: `10-Targets/Sentry.md`
- الريبورت (تحت المناقشة): `09-Writeups & Reports/Plan Restriction Bypass - Free Tier to Paid Features.md`

## References

- https://www.splunk.com

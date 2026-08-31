# Algolia

> خدمة **بحث سحابية** (Search-as-a-Service / SaaS) — الشركة بتبعت نسخة من بياناتها ليها، والبحث بيحصل من المتصفح مباشرة وفي أجزاء من الثانية. زي GraphQL و Ajax: **web API** بتتعامل معاها الفرونت إند، مش أداة infrastructure.

## فكرة بسيطة عنها

- الموقع بيبقى عنده قاعدة البيانات الأصلية، وبجانبها **Algolia** كمحرك بحث فائق السرعة.
- الـ Frontend بيبعث استعلامات البحث **مباشرة لـ Algolia** (من المتصفح) من غير ما يعدّي على سيرفر الموقع.
- عشان كده مفتاح البحث لازم يكون موجود في الكود اللي المتصفح بيستلمه (الـ JS bundle) — **ده بالتصميم مش ثغرة**.

## مصطلحات مهمة (اللي بتيجي في الريبورتس)

| المصطلح | معناه |
|---------|-------|
| `appId` | رقم حساب الشركة على Algolia (مش سر) |
| `apiKey` | مفتاح API — **search-only keys** مصممة تكون public، **admin keys** سريّة |
| `index` | جدول في قاعدة بيانات — البيانات بتتقسّم على فهارس (زي `prod_..._talent_v0`) |
| `X-Algolia-Application-Id` + `X-Algolia-API-Key` | الـ Headers بتاعة الـ authentication في كل طلب |
| `-dsn.algolia.net` | الـ DSN endpoint — سطح البحث/القراءة (read-only). `.algolia.net` = الـ API الرئيسي/الإداري |
| `attributesToRetrieve` | الحقول اللي الطلب بيرجّعها — **لو اتسابت مش مذكورة، بيرجّع كل الحقول** (السلوك الافتراضي) |
| `filters` | فلترة بالصيغة `field:value` — بتشتغل بس على الحقول اللي المطور فعّلها في `attributesForFaceting` |
| `facets` | تجميع إحصائي للقيم (كام male / female / non_binary...) مع `maxValuesPerFacet` |
| `hitsPerPage` | عدد النتائج المطلوبة — `0` بترجّع الـ metadata بس |
| `nbHits` | إجمالي عدد النتائج المطابقة — بييجي في الـ metadata مع أي استجابة |
| `GET /1/indexes` | بيرجّع كل الـ indexes اللي المفتاح يقدّر يوصلها (enumeration من غير تخمين) |

## ليه هي مهمة في سياق Bug Bounty؟

- **الـ Key موجود في الـ JS بالتصميم** — فالمشكلة مش وجوده، المشكلة في **الصلاحيات اللي عليه**:
  - هل بيقدر يجيب حقول داخلية بالاسم؟ (اختبار بـ `attributesToRetrieve`)
  - هل بيقدر يفلتر بحقول إدارية؟ (اختبار بـ `filters`)
  - هل مقصور على index واحد ولا يفتح كل الـ indexes؟ (اختبار بـ `GET /1/indexes`)
- أسماء الحقول الحساسة بتتعرف من **السلوك الافتراضي**: استعلام من غير `attributesToRetrieve` بيرجّع السجل كامل — تقرا الـ JSON الخام وتشوف الحقول بعينك.
- **الـ Fix الصحيح**: `unretrievableAttributes` (حقول مش قابلة للاسترجاع) + **Secured API Keys** (قيد المفتاح العام بفلاتر/حقول مدمجة) + عدم وضع الحقول الحساسة في الـ index أصلاً + منع ملفات الـ source map في الـ production.

## فين بيظهر في الريبو

- الريبورت: `09-Writeups & Reports/Algolia Search Key Over-Exposure - 154k Records.md`

## References

- https://www.algolia.com
- [Algolia API documentation](https://www.algolia.com/doc/)
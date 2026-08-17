# Target: Sentry

> Error tracking & performance monitoring platform — اللي مذكور في ريبورت ExamenTry (اسم مستعار، التارجت الحقيقي هو Sentry على الأغلب حسب شكل الـ API والبنية).

## Info

- **النوع:** SaaS — error tracking / crash reporting / performance monitoring للـ applications.
- **بيستخدموه إزاي:** المطور بيدخل حاجة اسمها **DSN** في الكود، وبيت بعث الـ errors/events للمنصة عشان يتعرضلها ويراقبها.
- **البنية (اللي بتظهر في الريبورتس):**
  - Subdomain لكل منظمة: `yoursubdomain.sentry.io` / `us.sentry.io`
  - REST API: `/api/0/projects/{org}/{project}/plugins/{plugin}/`
  - الـ Plugins/integrations: ميزة "بيانات بتتبعت لمكان تاني" زي Splunk (Data Forwarding).
  - الـ Settings صفحات: `/settings/projects/{project}/plugins/...`

## Attack Surface المعتاد

- **Plan/feature gating:** ميزات مدفوعة (زي data forwarding) لازم تتشيك عليها على السيرفر، مش في الـ UI بس.
- **Permissions منظمة/بروجكت:** هل المستخدم يقدّر يعدل بروجكت مش بتاعه؟ (access control)
- **Plugins config:** أوبشنز الـ plugins بتتسجل على إيه وإزاي.

## Reports من جوا الريبو

| Report | Link / File | ملخص |
|--------|------------|------|
| Plan Restriction Bypass (ExamenTry) | `09-Writeups & Reports/Plan Restriction Bypass - Free Tier to Paid Features.md` | فري يوزر بيوصّل لـ data forwarding (ميزة مدفوعة) عن طريق request مباشر للـ API من غير check على البلان |

## External Sources

- الموقع الرسمي: https://sentry.io
- الـ API docs: https://docs.sentry.io/api/

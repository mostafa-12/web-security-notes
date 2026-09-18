"""Lab-09 data layer: a micro-cached GraphQL orders endpoint.

The pattern (from the writeup): the first GetOrders hits the DB, everyone
else in the same 3-4s window gets the cached copy. Short TTL is deliberate
and fine. The bug: a USER-SPECIFIC response is cached under a key with NO
auth context, so one shop's orders are served to anyone who asks in time.

A background thread plays the victim: every VICTIM_POLL_EVERY seconds their
dashboard refreshes and re-primes the cache (TTL = CACHE_TTL seconds).
"""
import threading
import time

from config import CACHE_TTL, VICTIM_POLL_EVERY, TOKENS, FLAG

ORDERS = {
    "shop-123": [  # victim shop - the target
        {"order": "ord-9001", "customer": "victim@shop.local", "total": 4200,
         "note": FLAG},
        {"order": "ord-9002", "customer": "buyer2@shop.local", "total": 150},
    ],
    "shop-999": [],  # attacker's own (empty) shop
}

_cache = {}  # (operation, shop_id) -> (body, expires_at)
_lock = threading.Lock()


def _db_fetch(shop_id):
    time.sleep(0.05)  # the DB hit the cache exists to avoid
    return {"shop": shop_id, "orders": ORDERS.get(shop_id, [])}


def get_orders(token, shop_id):
    """Serve GetOrders. Returns (body, status, cache_header)."""
    key = ("GetOrders", shop_id)
    now = time.time()
    with _lock:
        hit = _cache.get(key)
        if hit and hit[1] > now:
            # VULN: cached authorized data served with ZERO auth check.
            # Whoever asks inside the window gets the victim's response.
            return hit[0], 200, "HIT"
    # Cache miss: the real authorization decision happens here...
    if TOKENS.get(token) != shop_id:
        return {"error": "forbidden: not your shop"}, 403, "MISS"
    body = _db_fetch(shop_id)
    with _lock:
        _cache[key] = (body, now + CACHE_TTL)
    return body, 200, "MISS"


def _victim_loop():
    """Background victim: a dashboard left open on auto-refresh."""
    while True:
        time.sleep(VICTIM_POLL_EVERY)
        body = _db_fetch("shop-123")
        with _lock:
            _cache[("GetOrders", "shop-123")] = (body, time.time() + CACHE_TTL)


threading.Thread(target=_victim_loop, daemon=True).start()

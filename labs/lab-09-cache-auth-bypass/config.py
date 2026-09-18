"""Lab-09 settings."""
PORT = 8009
FLAG = "FLAG{auth_not_in_cache_key_3s_window}"
# Micro-cache TTL (seconds) - the vulnerable window from the writeup (3-4s)
CACHE_TTL = 4
# How often the victim dashboard auto-refreshes (re-primes the cache)
VICTIM_POLL_EVERY = 15
TOKENS = {"victim-token": "shop-123", "attacker-token": "shop-999"}

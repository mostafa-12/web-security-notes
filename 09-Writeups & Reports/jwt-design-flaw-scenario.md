# JWT Design Flaw Scenario - Recreation

## Vulnerable Authentication Flow

```
┌─────────────┐     Login (credentials)      ┌─────────────┐
│   Client    │ ───────────────────────────▶ │   Backend   │
│  (Browser)  │                              │             │
└─────────────┘                              └──────┬──────┘
                                                     │
                                                     │ Issues refresh JWT
                                                     │ Set-Cookie: __Host-refreshToken=<JWT>
                                                     │ (HttpOnly, Secure, SameSite=Strict)
                                                     ▼
┌─────────────┐ ◀─────────────────────────── ┌─────────────┐
│   Client    │                              │   Backend   │
│  (Browser)  │                              │             │
└─────────────┘                              └─────────────┘
                                                     │
                  Subsequent Requests               │
┌─────────────┐     Cookie: __Host-refreshToken    ┌──────┬──────┘
│   Client    │ ─────────────────────────────────▶ │    │
│  (Browser)  │                                    │    │
└─────────────┘                                    │    │
                                                   │    │ Validates JWT signature only
                                                   │    │ Extracts `sub` claim
                                                   │    │ Treats as authenticated user
                                                   │    │ NO server-side session check
                                                   │    │ NO jti validation
                                                   │    │ NO rotation
                                                   ▼    ▼
```

## Vulnerable Backend Implementation (Pseudo-code)

```python
# ❌ VULNERABLE: Stateless refresh token validation
@app.route("/api/refresh", methods=["POST"])
def refresh_access_token():
    refresh_token = request.cookies.get("__Host-refreshToken")
    
    if not refresh_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # ONLY validates signature + exp
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        
        # NO server-side session lookup!
        # NO jti check against revocation list!
        # NO device/organization context validation!
        
        user_id = payload["sub"]
        
        # Issues new access token based solely on `sub`
        access_token = generate_access_token(user_id)
        
        return jsonify({"access_token": access_token})
        
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


@app.route("/api/protected", methods=["GET"])
def protected_resource():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        
        # Trusts the token completely - no additional validation
        return jsonify({"data": f"Welcome user {user_id}"})
        
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
```

## The Refresh Token Payload (Decoded)

```json
{
  "sub": "user_12345",
  "iat": 1737900000,
  "exp": 1738500000
}
```

**Missing claims:** `iss`, `aud`, `jti`, `device_id`, `org_id`, `session_id`

## Attack Scenario: Token Compromise → Account Takeover

```
Attacker steals refresh token (XSS, MITM, logs, etc.)
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│ Attacker sends request with stolen __Host-refreshToken │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
        Backend validates signature ✓
        Extracts `sub`: "user_12345" ✓
        Token not expired ✓
                    │
                    ▼
        ┌─────────────────────────┐
        │ ISSUES NEW ACCESS TOKEN │  ← Full account takeover
        │ FOR user_12345          │     Zero-click, persistent
        └─────────────────────────┘
                    │
                    ▼
        Attacker accesses ALL protected resources
        Until token expires (6 days in example)
```

## Why Removing Other Cookies Still Works

```python
# The test the author did:
# 1. Login → get: refresh_token + session_cookie + platform_cookies
# 2. Delete ALL cookies EXCEPT __Host-refreshToken
# 3. Navigate to protected page
# 4. Page loads successfully → proves refresh token alone = auth

# Backend logic:
def get_current_user(request):
    # Only looks at refresh token, ignores session_cookie entirely
    refresh_token = request.cookies.get("__Host-refreshToken")
    if refresh_token:
        payload = jwt.decode(refresh_token, SECRET_KEY)
        return User.get(payload["sub"])  # No session validation!
    return None
```

## Root Cause: Single Source of Truth

| Component | Trusted? | Validated? |
|-----------|----------|------------|
| JWT Signature | ✅ Yes | ✅ Yes |
| `exp` claim | ✅ Yes | ✅ Yes |
| `sub` claim | ✅ Yes | ❌ **No cross-reference** |
| Server-side session | ❌ **No** | ❌ **Not checked** |
| Token ID (`jti`) | ❌ **Absent** | ❌ **Can't revoke** |
| Device context | ❌ **Absent** | ❌ **No binding** |
| Rotation | ❌ **Absent** | ❌ **Replay possible** |

## Secure Implementation (Fixed)

```python
# ✅ SECURE: Server-side session binding + rotation
@app.route("/api/refresh", methods=["POST"])
def refresh_access_token():
    refresh_token = request.cookies.get("__Host-refreshToken")
    
    if not refresh_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        
        # 1. Validate standard claims
        if not validate_claims(payload, required=["iss", "aud", "jti", "sub", "exp"]):
            return jsonify({"error": "Invalid token claims"}), 401
        
        # 2. Server-side session lookup (CRITICAL)
        session = SessionStore.get(payload["jti"])
        if not session or session.revoked:
            # Token replay detected! Revoke entire session chain
            SessionStore.revoke_chain(payload["jti"])
            return jsonify({"error": "Token revoked"}), 401
        
        # 3. Validate context binding
        if session.user_id != payload["sub"]:
            return jsonify({"error": "Token mismatch"}), 401
        if session.device_fingerprint != get_device_fingerprint(request):
            return jsonify({"error": "Device mismatch"}), 401
        
        # 4. ROTATE: Invalidate old, issue new
        SessionStore.revoke(payload["jti"])
        new_jti = generate_jti()
        SessionStore.create(
            jti=new_jti,
            user_id=payload["sub"],
            device_fingerprint=get_device_fingerprint(request),
            expires_at=datetime.now() + REFRESH_TTL
        )
        
        new_refresh_token = jwt.encode({
            "sub": payload["sub"],
            "jti": new_jti,
            "iss": "myapp",
            "aud": "myapp-client",
            "iat": time.time(),
            "exp": time.time() + REFRESH_TTL
        }, SECRET_KEY)
        
        # Set new refresh token cookie
        response = jsonify({"access_token": generate_access_token(payload["sub"])})
        response.set_cookie("__Host-refreshToken", new_refresh_token, 
                           httponly=True, secure=True, samesite="Strict")
        return response
        
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
```

## Key Fixes Summary

| Fix | Why It Matters |
|-----|----------------|
| **Server-side session store** | Token alone ≠ auth; session must exist & be active |
| **`jti` (JWT ID)** | Unique ID per token → targeted revocation, replay detection |
| **Refresh token rotation** | Old token invalidated on use → stolen token becomes useless |
| **Device/organization binding** | Context validation prevents cross-device/org misuse |
| **Standard claims (`iss`, `aud`)** | Prevents token confusion across services |
| **Reuse detection → full chain revocation** | Detects theft immediately, kills attacker's access |

"""Lab-11 auth layer: HS256 JWT issue + verify (stdlib only).

The crypto is CORRECT here - that is the point of the writeup. The server
verifies the signature on every request. The bug is one layer up: TOKEN
ISSUANCE hands a low-privilege Editor the exact scopes the roles endpoint
authorizes on. The check exists; the token is over-granted.
"""
import base64
import hashlib
import hmac
import json
import time

from config import SECRET, USERS


def b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def issue(username):
    profile = USERS[username]
    header = b64e(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = b64e(json.dumps({"sub": profile["sub"], "role": profile["role"],
                               "scopes": profile["scopes"],
                               "iat": int(time.time()),
                               "exp": int(time.time()) + 3600}).encode())
    sig = b64e(hmac.new(SECRET, f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"


def verify(token):
    """Verify signature + expiry. Returns claims or None."""
    try:
        header, payload, sig = token.split(".")
        good = b64e(hmac.new(SECRET, f"{header}.{payload}".encode(),
                             hashlib.sha256).digest())
        if not hmac.compare_digest(good, sig):
            return None
        claims = json.loads(b64d(payload))
        if claims.get("exp", 0) < time.time():
            return None
        return claims
    except Exception:
        return None

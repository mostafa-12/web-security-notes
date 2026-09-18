"""Lab-08 auth layer: hand-rolled HMAC-SHA256 JWTs, validated the WRONG way.

What is checked:  signature + exp.
What is missing:  jti / session store / rotation / device binding / iss / aud.
Because of that, whoever holds a refresh token IS the user until it expires.

Compare with the fixed version in:
  09-Writeups & Reports/jwt-design-flaw-scenario.md  (Secure Implementation)
"""
import base64
import hashlib
import hmac
import json
import time

from config import SECRET, REFRESH_TTL


def b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def make_jwt(sub, ttl=REFRESH_TTL):
    header = b64e(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = b64e(json.dumps({"sub": sub, "iat": int(time.time()),
                               "exp": int(time.time()) + ttl}).encode())
    sig = b64e(hmac.new(SECRET, f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"


def verify_sig_only(token):
    """Validate signature + expiry ONLY. Returns the payload or None.

    VULN: no server-side session lookup, no jti, no rotation, no context
    binding. A stolen token replays cleanly until `exp`.
    """
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


def mint_access_token(sub):
    """Issue an access token based solely on `sub` - no session check."""
    return (b64e(json.dumps({"alg": "none"}).encode()) + "."
            + b64e(json.dumps({"sub": sub, "scope": "full"}).encode()) + ".lab")


def read_access_token(token):
    """Decode our lab access token. Returns the payload or None."""
    try:
        return json.loads(b64d(token.split(".")[1]))
    except Exception:
        return None


def refresh_token_from(cookie_header):
    """Pull __Host-refreshToken out of a Cookie header."""
    for part in (cookie_header or "").split(";"):
        if "__Host-refreshToken" in part:
            return part.split("=", 1)[1].strip()
    return ""

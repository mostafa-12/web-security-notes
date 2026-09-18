#!/usr/bin/env python3
"""Lab-08: JWT refresh design flaw - signature-only validation (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8008

The backend treats the refresh JWT as the session itself (see auth.py).
Prove it: log in, delete every cookie except __Host-refreshToken, and you
are still authenticated. Then replay a stolen victim token (see /leak-demo).
"""
from flask import Flask, request, jsonify, make_response

import auth
import config

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({"lab": "jwt refresh flaw",
                    "login": 'POST /login {"user":"victim"} -> Set-Cookie __Host-refreshToken',
                    "test": "delete every cookie EXCEPT __Host-refreshToken, then GET /api/refresh",
                    "attack": "steal victim refresh token (see /leak-demo), replay it as attacker"})


@app.get("/leak-demo")
def leak_demo():
    # Simulates a token stolen via XSS/logs - in real life the attacker
    # steals it; here we show it so the lab is solvable.
    return jsonify({"note": "simulated leak (XSS/log/MITM)",
                    "stolen_refresh": auth.make_jwt(config.VICTIM)})


@app.get("/api/refresh")
def refresh():
    claims = auth.verify_sig_only(auth.refresh_token_from(request.headers.get("Cookie")))
    if not claims:
        return jsonify({"error": "invalid/expired refresh"}), 401
    # VULN: access issued solely from `sub`, no session lookup (see auth.py).
    out = {"access_token": auth.mint_access_token(claims["sub"]), "user": claims["sub"]}
    if claims["sub"] == config.VICTIM:
        out["victim_data"] = {"email": "victim@lab.local", "flag": config.FLAG}
    return jsonify(out)


@app.get("/api/protected")
def protected():
    claims = auth.read_access_token(request.headers.get("Authorization", "").replace("Bearer ", ""))
    if not claims:
        return jsonify({"error": "bad access token"}), 401
    if claims.get("sub") == config.VICTIM:
        return jsonify({"data": f"Welcome {config.VICTIM}", "flag": config.FLAG})
    return jsonify({"data": f"Welcome {claims.get('sub')}"})


@app.post("/login")
def login():
    user = (request.get_json(silent=True) or {}).get("user", config.VICTIM)
    resp = make_response(jsonify({"logged_in": user}))
    resp.set_cookie("__Host-refreshToken", auth.make_jwt(user), path="/",
                    httponly=True, secure=True, samesite="Strict")
    return resp


if __name__ == "__main__":
    print(f"[lab-08] http://127.0.0.1:{config.PORT}")
    app.run(host="127.0.0.1", port=config.PORT)

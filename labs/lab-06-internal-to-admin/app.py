#!/usr/bin/env python3
"""Lab-06: Internal User -> Admin via role-granting endpoint (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8006
Tokens: Authorization: Bearer internal-token (low priv) | Bearer admin-token

Vuln: POST /api/v1/contacts accepts companyUserRoles without checking the
      requester's role. Compare it with POST /api/v1/companyjoinrequests
      (the low-priv flow, which carries no roles parameter at all).
"""
from flask import Flask, request, jsonify

import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({"info": "SaaS invite lab",
                    "internal_flow": "POST /api/v1/companyjoinrequests (no roles param)",
                    "admin_flow": "POST /api/v1/contacts (takes companyUserRoles[])",
                    "tokens": {"admin": "admin-token", "internal": "internal-token"}})


@app.post("/api/v1/companyjoinrequests")
def join_request():
    if not store.role_of(request.headers.get("Authorization")):
        return jsonify({"error": "login required"}), 401
    return jsonify({"status": "join request created (low-priv, no role)"})


@app.post("/api/v1/contacts")
def contacts():
    role = store.role_of(request.headers.get("Authorization"))
    if not role:
        return jsonify({"error": "login required"}), 401
    payload, status = store.invite_contact(role, request.get_json(silent=True) or {})
    return jsonify(payload), status


if __name__ == "__main__":
    print(f"[lab-06] http://127.0.0.1:{config.PORT}")
    app.run(host="127.0.0.1", port=config.PORT)

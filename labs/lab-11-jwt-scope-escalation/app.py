#!/usr/bin/env python3
"""Lab-11: Unauthorized Role Management via over-privileged JWT (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8011

The UI shows "Roles & permissions: disabled" for Editors. But YOUR OWN
JWT carries dp.entitlements.plans.read/write - the exact scopes the
backend authorizes the roles endpoint on. Decode the token, then call
the endpoint the UI hides.
"""
from flask import Flask, request, jsonify, render_template

import auth
import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login")
def login():
    user = (request.get_json(silent=True) or {}).get("user", "editor")
    if user not in config.USERS:
        return jsonify({"error": "unknown user (try editor)"}), 404
    return jsonify({"token": auth.issue(user), "role": config.USERS[user]["role"]})


@app.post("/development/entitlements/roles")
def create_role():
    claims = auth.verify(request.headers.get("Authorization", "").replace("Bearer ", ""))
    if not claims:
        return jsonify({"error": "invalid token"}), 401
    payload, status = store.create_role(claims, request.get_json(silent=True) or {})
    return jsonify(payload), status


if __name__ == "__main__":
    print(f"[lab-11] http://127.0.0.1:{config.PORT}  login as editor, decode your JWT")
    app.run(host="127.0.0.1", port=config.PORT)

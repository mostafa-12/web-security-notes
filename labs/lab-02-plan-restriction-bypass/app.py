#!/usr/bin/env python3
"""Lab-02: Plan Restriction Bypass - free tier -> paid data forwarding (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8002
Login as free user (no password in lab): X-User: free  | paid user: X-User: paid

Vuln: UI hides Splunk forwarding for free plan, but the settings page AND
      PUT /api/0/.../plugins/splunk/ have no server-side plan check.
"""
import json

from flask import Flask, request, jsonify, render_template

import config
import store

app = Flask(__name__)


@app.get("/")
def dashboard():
    user = request.headers.get("X-User", "free")
    plan = "paid" if user == "paid" else "free"
    return render_template("dashboard.html", plan=plan, user=user)


@app.get("/settings/projects/proj-123/plugins/splunk/")
def settings_page():
    user = request.headers.get("X-User", "free")
    # VULN: page loads for free tier too (no plan check)
    return render_template("settings.html", user=user,
                           current=json.dumps(store.get_forwarding()))


@app.route("/api/0/projects/org-1/proj-123/plugins/splunk/", methods=["GET", "PUT"])
def splunk_api():
    user = request.headers.get("X-User", "free")
    if request.method == "GET":
        return jsonify(store.get_forwarding())
    cfg = request.get_json(silent=True) or {}
    return jsonify(store.enable_forwarding(cfg, user))


if __name__ == "__main__":
    print(f"[lab-02] http://127.0.0.1:{config.PORT}  use header X-User: free")
    app.run(host="127.0.0.1", port=config.PORT)

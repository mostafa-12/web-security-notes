#!/usr/bin/env python3
"""Lab-03: API Misconfiguration - PII leak via stray JS + non-expiring invites (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8003
Auth: header X-Session: <any-logged-in-user> (alice / bob / attacker).

Vuln: GET /manager/api/brainstorms/{uuid}/participants checks login but NOT
      membership. Invite codes in static/55932.js (live) + /archive/55932.js
      (old rotated codes, still valid because invites never expire).
"""
from flask import Flask, request, jsonify, render_template, Response

import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/archive/55932.js")
def archive_js():
    # Simulates the Wayback snapshot: an old copy of the same bundle that
    # still contains the rotated-out code.
    return Response(store.ARCHIVE_JS, mimetype="application/javascript")


@app.get("/manager/api/brainstorms/<uuid>/participants")
def participants(uuid):
    if not request.headers.get("X-Session"):
        return jsonify({"error": "login required"}), 401
    dump = store.dump_participants(uuid)
    if dump is None:
        return jsonify({"error": "board not found"}), 404
    return jsonify(dump)


@app.post("/join/<code>")
def join(code):
    uuid, err = store.join_with_code(code, request.headers.get("X-Session"))
    if err:
        return jsonify({"error": err}), 404
    return jsonify({"joined": True, "board_uuid": uuid, "code": code})


if __name__ == "__main__":
    print(f"[lab-03] http://127.0.0.1:{config.PORT}  use header X-Session: attacker")
    app.run(host="127.0.0.1", port=config.PORT)

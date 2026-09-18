#!/usr/bin/env python3
"""Lab-01: Training Platform - login bypass to full admin (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py  -> http://127.0.0.1:8001

Layout (same pattern in every lab):
  config.py      settings (port, flag, constants)
  store.py       fake database + business logic (the-domain layer)
  static/        JS bundles, as a real app would serve them
  templates/     HTML pages (Jinja2)
  app.py         routes only - thin handlers, no business logic here

Vulns to find: (1) trailing-slash bypass  (2) double-path error leak
               (3) client-side readOnly flag 1->0
"""
import json

from flask import Flask, request, jsonify, render_template

import config
import store

app = Flask(__name__)


@app.after_request
def add_powered_by(resp):
    resp.headers["X-Powered-By"] = "ASP.NET"
    return resp


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/ReportServer")
def report_server():
    return render_template("report_server.html")


@app.get("/ReportServer/Content_Usage")
def content_usage():
    return render_template("content_usage.html")


@app.get("/scripts/views/courses/index.js")
def courses_js():
    # Original deep URL, served from static/ like a real bundle would be.
    return app.send_static_file("courses-index.js")


@app.get("/scripts/views/users/index.js")
def users_js():
    return app.send_static_file("users-index.js")


@app.get("/app/region/east/Users.aspx/Users.aspx/manageUserProfile")
def double_path():
    # Bypass #2b: double path leaks the real path in an error
    return render_template("double_path_error.html"), 500


@app.get("/app/region/east/users.aspx")
def blocked():
    # Bypass #2: exact path blocked ...
    return render_template("blocked.html"), 401


@app.get("/app/region/east/users.aspx/")
def with_slash():
    # ... but trailing slash allowed (canonicalization mismatch)
    return render_template("search.html")


@app.route("/app/region/east/Users.aspx/manageUserProfile", methods=["GET", "POST"])
def manage_profile():
    uid = request.args.get("userId", "1001")
    if request.method == "GET":
        # NO auth check, returns readOnly flag = 1 (client-side only)
        user = store.get_user(uid)
        profile = {"userId": uid, **user, "readOnly": 1}
        return render_template("edit_profile.html", uid=uid, user=user,
                               profile_json=json.dumps(profile))
    # VULN: no auth check + no server-side readOnly enforcement (see store.py).
    data = request.get_json(silent=True)
    if data is None:
        data = {"raw": request.form.get("name", request.get_data(as_text=True))}
    return jsonify(store.rename_user(uid, data.get("name")))


if __name__ == "__main__":
    print(f"[lab-01] http://127.0.0.1:{config.PORT}  (no login needed - that is the point)")
    app.run(host="127.0.0.1", port=config.PORT)

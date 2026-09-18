#!/usr/bin/env python3
"""Lab-04: Algolia-style Search Key Over-Exposure (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8004

Simulates a public search key with over-permissioned fields, filters,
facets, a 2nd index, and a leaked source map.
Key extraction: GET /dist/bundle-abc123.js  -> grep appId/apiKey/indexName
Search: POST /1/indexes/<index>/query with X-Algolia-Application-Id / X-Algolia-API-Key
"""
from flask import Flask, request, jsonify, render_template

import config
import store

app = Flask(__name__)


def _valid_key():
    # The key is public BY DESIGN - the bug is what it is allowed to do.
    return request.headers.get("X-Algolia-API-Key") == config.API_KEY


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/dist/bundle-abc123.js")
def bundle():
    # Original dist URL, served from static/ like a real build artifact.
    return app.send_static_file("bundle-abc123.js")


@app.get("/dist/server.js.map")
def server_map():
    # VULN: a SERVER-side source map deployed to production.
    resp = app.send_static_file("server.js.map")
    resp.mimetype = "application/json"
    return resp


@app.get("/1/indexes")
def list_indexes():
    # Index enumeration (the reliable route the article never mentions).
    if not _valid_key():
        return jsonify({"message": "invalid key"}), 403
    return jsonify(store.index_summary())


@app.post("/1/indexes/<index>/query")
def search(index):
    if not _valid_key():
        return jsonify({"message": "invalid key"}), 403
    payload, status = store.search(index, request.get_json(silent=True) or {})
    return jsonify(payload), status


if __name__ == "__main__":
    print(f"[lab-04] http://127.0.0.1:{config.PORT}")
    app.run(host="127.0.0.1", port=config.PORT)

#!/usr/bin/env python3
"""Lab-09: Authorization Bypass due to Cache Misconfiguration (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8009
Tokens: Authorization: Bearer attacker-token (your shop: shop-999)

A victim dashboard auto-refreshes every 15s; each refresh caches their
GetOrders response for 4s under a key with NO auth context. Poll the same
query as the attacker and catch the window: 403 normally, 200 + victim
orders on a cache HIT. The X-Cache header is your oracle.
"""
from flask import Flask, request, jsonify, render_template, make_response

import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/graphql")
def graphql():
    body = request.get_json(silent=True) or {}
    if body.get("operationName") != "GetOrders":
        return jsonify({"error": "unknown operation"}), 400
    shop_id = (body.get("variables") or {}).get("shop_id", "")
    data, status, cache = store.get_orders(
        request.headers.get("Authorization", "").replace("Bearer ", ""), shop_id)
    resp = make_response(jsonify(data), status)
    resp.headers["X-Cache"] = cache
    return resp


if __name__ == "__main__":
    print(f"[lab-09] http://127.0.0.1:{config.PORT}  use Bearer attacker-token, be patient (~15s cycle)")
    app.run(host="127.0.0.1", port=config.PORT)

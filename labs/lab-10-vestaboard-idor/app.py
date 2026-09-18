#!/usr/bin/env python3
"""Lab-10: Vestaboard-style IDOR x3 (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8010
You are u-bob: Authorization: Bearer bob-token (admin of board-1001 only).

Three IDORs, one root cause (identifiers treated as proof of access):
  1. GET /simulator/<board-id> - unauthenticated board read
  2. GraphQL updateUser(id:) - rename ANY user
  3. GraphQL updateMemberRole(role:) - Admin -> Owner by tampering the value
"""
import re

from flask import Flask, request, jsonify, render_template

import config
import store

app = Flask(__name__)


def caller():
    return config.TOKENS.get(request.headers.get("Authorization", "").replace("Bearer ", ""))


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/simulator/<board_id>")
def simulator(board_id):
    data = store.read_board(board_id)
    if data is None:
        return jsonify({"error": "board not found"}), 404
    return jsonify(data)


@app.get("/board/<board_id>/members")
def members(board_id):
    user = caller()
    if not user:
        return jsonify({"error": "login required"}), 401
    board = store.BOARDS.get(board_id)
    if not board:
        return jsonify({"error": "board not found"}), 404
    # The UI only offers "member" in the role dropdown for admins...
    return jsonify({"board": board_id, "members": board["members"],
                    "your_role": board["members"].get(user),
                    "assignable_roles": ["member"]})


@app.get("/board/<board_id>/billing")
def billing(board_id):
    user = caller()
    if not user:
        return jsonify({"error": "login required"}), 401
    payload, status = store.billing_page(board_id, user)
    return jsonify(payload), status


@app.post("/graphql")
def graphql():
    user = caller()
    if not user:
        return jsonify({"error": "login required"}), 401
    q = (request.get_json(silent=True) or {}).get("query", "")
    m = re.search(r'updateUser\s*\(\s*id\s*:\s*"([^"]+)"\s*,\s*name\s*:\s*"([^"]+)"', q)
    if m:
        payload, status = store.rename_user(m.group(1), m.group(2), user)
        return jsonify(payload), status
    m = re.search(r'updateMemberRole\s*\(\s*boardId\s*:\s*"([^"]+)"\s*,\s*userId\s*:\s*"([^"]+)"\s*,\s*role\s*:\s*"([^"]+)"', q)
    if m:
        payload, status = store.set_role(m.group(1), m.group(2), m.group(3), user)
        return jsonify(payload), status
    return jsonify({"error": "unknown mutation (try updateUser / updateMemberRole)"}), 400


if __name__ == "__main__":
    print(f"[lab-10] http://127.0.0.1:{config.PORT}  use Bearer bob-token")
    app.run(host="127.0.0.1", port=config.PORT)

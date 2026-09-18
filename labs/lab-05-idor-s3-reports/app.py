#!/usr/bin/env python3
"""Lab-05: IDOR + public S3 report exposure (async background job) - Flask.
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8005
Users: X-User: alice (owns posts 1-3) | X-User: bob (owns posts 4-6)

Flow: POST /api/reports/generate {postId} -> {backgroundJobId}
      -> GET /api/reports/result/{jobId} -> {downloadUrl on S3}
"""
from flask import Flask, request, jsonify, render_template, Response

import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    user = request.headers.get("X-User", "alice")
    return render_template("index.html", user=user)


@app.post("/api/reports/generate")
def generate():
    try:
        post_id = int((request.get_json(silent=True) or {}).get("postId", -1))
    except (TypeError, ValueError):
        return jsonify({"error": "bad postId"}), 400
    job_id, err = store.create_job(post_id)
    if err:
        return jsonify({"error": err}), 404
    return jsonify({"backgroundJobId": job_id, "status": "CREATED"})


@app.get("/api/reports/result/<job_id>")
def result(job_id):
    url, err = store.job_download_url(job_id)
    if err:
        return jsonify({"error": err}), 404
    return jsonify({"status": "COMPLETED", "downloadUrl": url})


@app.get("/s3-bucket/", strict_slashes=False)
def list_bucket():
    return jsonify(store.list_bucket())


@app.get("/s3-bucket/report/<job_id>.pdf")
def download(job_id):
    body = store.read_object(job_id)
    if body is None:
        return Response("no such file", status=404, mimetype="text/plain")
    return Response(body, mimetype="application/pdf")


if __name__ == "__main__":
    print(f"[lab-05] http://127.0.0.1:{config.PORT}  X-User: alice / bob")
    app.run(host="127.0.0.1", port=config.PORT)

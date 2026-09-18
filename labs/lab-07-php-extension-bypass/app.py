#!/usr/bin/env python3
"""Lab-07: Auth bypass via .php extension removal + directory listing (Flask).
Setup: pip install -r ../requirements.txt
Run (from this folder): python app.py -> http://127.0.0.1:8007

Vuln: /videos.php requires Cookie session=admin, /videos serves the SAME
      content with no check. Plus /media/ directory listing and a custom
      404 page that leaks the site map.
"""
from flask import Flask, request, Response, render_template

import config
import store

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/img/x.svg")
def svg():
    return Response('<svg xmlns="http://www.w3.org/2000/svg"><rect width="50" height="50"/></svg>',
                    mimetype="image/svg+xml")


@app.get("/videos.php")
def videos_protected():
    if "session=admin" not in request.headers.get("Cookie", ""):
        return Response("<h1>Login required</h1><p>/videos.php needs auth.</p>",
                        status=403, mimetype="text/html")
    return render_template("videos.html", rows=store.video_rows(), flag=config.FLAG)


@app.get("/videos")
def videos_open():
    # VULN: same resource, no auth check (router normalizes, middleware doesn't)
    return render_template("videos.html", rows=store.video_rows(), flag=config.FLAG)


@app.get("/media/", strict_slashes=False)
def media_listing():
    # VULN: directory listing enabled
    return render_template("media_listing.html", rows=store.video_rows())


@app.get("/media/<path:fname>")
def media_file(fname):
    if fname.endswith(".mp4"):
        return Response(store.media_bytes(f"/media/{fname}"), mimetype="video/mp4")
    return render_template("not_found.html"), 404


@app.errorhandler(404)
def leaked_404(e):
    return render_template("not_found.html"), 404  # custom 404 leaks /videos.php


if __name__ == "__main__":
    print(f"[lab-07] http://127.0.0.1:{config.PORT}")
    app.run(host="127.0.0.1", port=config.PORT)

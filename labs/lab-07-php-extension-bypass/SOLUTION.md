# SOLUTION — Lab-07

```bash
curl http://127.0.0.1:8007/img/x.svg
curl http://127.0.0.1:8007/img/y.svg          # custom 404 -> leaks /videos.php
curl -i http://127.0.0.1:8007/videos.php      # 403 login required
curl -i http://127.0.0.1:8007/videos          # 200 FULL ACCESS (extension removal)
curl http://127.0.0.1:8007/media/             # directory listing -> all files
curl http://127.0.0.1:8007/media/video1/video1.mp4
```

**Root cause:** the middleware matches `/videos.php` literally while the router normalizes `/videos` to the same app.
**Fix:** auth check on the resource/handler, not on the URL string + disable directory listing + generic 404 page.

"""Lab-07 data layer: the video catalog.

Two findings, one root-cause class (components interpreting the same
request differently):
  1. the auth middleware matches "/videos.php" literally while the router
     serves the same handler at "/videos" with no check
  2. /media/ ships with directory listing enabled
"""
from config import FLAG, VIDEOS


def video_rows():
    """<li> rows for the videos page and the directory listing."""
    return [{"name": v, "url": f"/media/{v}/{v}.mp4"} for v in VIDEOS]


def media_bytes(path):
    """Fake mp4 bytes for any file under /media/."""
    return f"FAKE MP4 BYTES for {path} {FLAG}".encode()

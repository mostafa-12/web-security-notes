"""Lab-05 data layer: posts, background jobs, and the fake S3 bucket.

Three trust boundaries live here, and all three fail open:
  API layer      POST /api/reports/generate never checks post ownership
  result layer   GET /api/reports/result/{jobId} never checks job ownership
  storage layer  the "S3 bucket" serves objects publicly + allows listing
"""
import uuid

from config import FLAG, PORT

POSTS = {1: "alice", 2: "alice", 3: "alice", 4: "bob", 5: "bob", 6: "bob"}
JOBS = {}  # jobId -> postId


def create_job(post_id):
    """Start a background report job. Returns (job_id, error)."""
    if post_id not in POSTS:
        return None, "post not found"
    # VULN: ownership never checked - anyone gets a job for anyone's post.
    job_id = str(uuid.uuid4())
    JOBS[job_id] = post_id
    return job_id, None


def job_download_url(job_id):
    """Result lookup. Returns (download_url, error)."""
    if job_id not in JOBS:
        return None, "job not found"
    # VULN: no check that the job belongs to the requester.
    return f"http://127.0.0.1:{PORT}/s3-bucket/report/{job_id}.pdf", None


def list_bucket():
    """Fake S3 ListBucket. VULN: open to anonymous callers."""
    return {"bucket": "companyname", "keys": [f"report/{j}.pdf" for j in JOBS]}


def read_object(job_id):
    """Fake S3 GetObject. VULN: objects are public-read, no auth at all."""
    post = JOBS.get(job_id)
    if not post:
        return None
    owner = POSTS.get(post, "?")
    extra = f" {FLAG}" if post in (4, 5, 6) else ""
    return f"PRIVATE REPORT post={post} owner={owner} secret-data-{post}{extra}"

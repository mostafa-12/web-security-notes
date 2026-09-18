"""Lab-08 settings."""
PORT = 8008
SECRET = b"lab-secret-key-change-me"
FLAG = "FLAG{refresh_token_is_not_a_session}"
VICTIM = "user_12345"
# refresh lifetime: 6 days (stolen token = 6 days of access)
REFRESH_TTL = 6 * 24 * 3600

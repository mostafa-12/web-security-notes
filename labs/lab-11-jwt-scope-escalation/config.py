"""Lab-11 settings."""
PORT = 8011
FLAG = "FLAG{scopes_in_token_beat_ui_disabled}"
SECRET = b"lab-11-secret"
# What the issuer puts in each role's token. The Editor's extra scopes
# are the planted bug: the UI hides role management, but the token
# carries the exact scopes the backend authorizes on.
USERS = {
    "editor": {"sub": "u-editor", "role": "Backoffice Editor",
               "scopes": ["dp.entitlements.plans.read", "dp.entitlements.plans.write"]},
    "admin": {"sub": "u-admin", "role": "Administrator",
              "scopes": ["dp.entitlements.plans.read", "dp.entitlements.plans.write",
                         "dp.entitlements.roles.read", "dp.entitlements.roles.write"]},
}

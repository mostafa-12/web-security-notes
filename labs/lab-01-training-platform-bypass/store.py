"""Lab-01 data layer: a fake user database + the operations on it.

In a real app this would be SQLAlchemy models. Here it is a dict so the
lab stays dependency-free (Flask only) and easy to read.
"""
from config import FLAG

# Fake user DB (50k in the real story -> 3 here for the lab)
USERS = {
    "1001": {"name": "Alice Admin", "email": "alice@platform.local", "ssn": "111-11-1001"},
    "1002": {"name": "Bob Trainer", "email": "bob@platform.local", "ssn": "111-11-1002"},
    "1003": {"name": "Carol Student", "email": "carol@platform.local", "ssn": "111-11-1003"},
}


def get_user(uid):
    """Return the user dict or a placeholder for unknown ids."""
    return USERS.get(uid, {"name": "Unknown", "email": "?", "ssn": "?"})


def rename_user(uid, new_name):
    """Update a user's name. Returns the flag: any write = full compromise.

    VULN: the route calls this with NO auth check and NO server-side
    readOnly enforcement. The read-only flag lives in JS only.
    """
    if uid in USERS and new_name is not None:
        USERS[uid]["name"] = new_name
    return {"status": "saved", "userId": uid, "flag": FLAG,
            "note": "Write access granted with ZERO credentials."}

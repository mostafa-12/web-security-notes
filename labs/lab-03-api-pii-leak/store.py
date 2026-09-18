"""Lab-03 data layer: boards, invite codes, participants.

In a real app these would be Board / Membership / User tables. Here dicts.
Two facts combine into the incident:
  1. the participants endpoint never checks membership (auth != authz)
  2. invite codes never expire, so even rotated codes stay valid forever
"""
from config import FLAG

BOARDS = {
    "11111111-1111-1111-1111-111111111111": {
        "code": "HTEN234S", "members": ["alice"],
        "participants": [
            {"email": "alice@lab.local", "name": "Alice", "uuid": "u-1"},
            {"email": "victim1@lab.local", "name": "Victim One", "uuid": "u-2"},
            {"email": "victim2@lab.local", "name": "Victim Two", "uuid": "u-3",
             "flag": FLAG},
        ],
    },
    "22222222-2222-2222-2222-222222222222": {
        "code": "OLDCODE9", "members": ["bob"],
        "participants": [
            {"email": "bob@lab.local", "name": "Bob", "uuid": "u-9"},
            {"email": "victim3@lab.local", "name": "Victim Three", "uuid": "u-10"},
        ],
    },
}
CODE_TO_BOARD = {v["code"]: k for k, v in BOARDS.items()}

# What's inside the stray live bundle (static/55932.js). The rotated-out
# code lives only in the archived copy served at /archive/55932.js.
LIVE_CODES = ["HTEN234S"]
ARCHIVED_CODES = ["HTEN234S", "OLDCODE9"]
ARCHIVE_JS = """// snapshot 2023 - go.target.com/55932.js
var INVITE_CODES = ["HTEN234S","OLDCODE9"];
"""


def find_board(uuid):
    return BOARDS.get(uuid)


def join_with_code(code, session):
    """Redeem an invite code. Returns (board_uuid, error).

    VULN (multiplier): invites never expire - a code removed from the live
    bundle still redeems, because validity is never time-boxed or revoked.
    """
    uuid = CODE_TO_BOARD.get(code)
    if not uuid:
        return None, "bad code"
    BOARDS[uuid]["members"].append(session or "attacker")
    return uuid, None


def dump_participants(uuid):
    """Return every participant of a board.

    VULN (root cause): no membership check - ANY logged-in user dumps ANY
    board. The route checks authentication; authorization is missing.
    """
    board = BOARDS.get(uuid)
    if not board:
        return None
    return {"board": uuid, "count": len(board["participants"]),
            "participants": board["participants"]}

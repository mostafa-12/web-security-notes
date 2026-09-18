"""Lab-10 data layer: boards, users, memberships.

The platform's whole authorization model is "knowing the identifier":
board IDs, user IDs and role names are accepted as proof of access and
never correlated back to the authenticated JWT. Three IDORs fall out:
  1. /simulator/<board-id> serves any board with no auth at all
  2. GraphQL updateUser(id:) renames ANY user (id swap)
  3. GraphQL updateMemberRole accepts role:"owner" from a mere admin
"""
from config import FLAG_READ, FLAG_ROLE

USERS = {
    "u-alice": {"name": "Alice Owner", "email": "alice@boards.local"},
    "u-bob": {"name": "Bob Member", "email": "bob@boards.local"},
}
BOARDS = {
    # the attacker's own board (admin member) - for baseline + privesc
    "board-1001": {"title": "Bob's side project",
                   "history": ["msg: hello world"],
                   "members": {"u-bob": "admin", "u-alice": "owner"},
                   "billing": "card **** 1001"},
    # the victim board - history holds the flag
    "board-2002": {"title": "Alice's secret board",
                   "history": ["msg: launch plan", f"msg: {FLAG_READ}"],
                   "members": {"u-alice": "owner"},
                   "billing": "card **** 2002"},
}


def read_board(board_id):
    """Simulator read. VULN #1: no auth whatsoever."""
    board = BOARDS.get(board_id)
    if not board:
        return None
    return {"board": board_id, "title": board["title"], "history": board["history"]}


def rename_user(target_id, new_name, caller_id):
    """GraphQL updateUser. VULN #2: id is trusted, never checked vs caller."""
    if target_id not in USERS:
        return {"error": "user not found"}, 404
    USERS[target_id]["name"] = new_name
    out = {"renamed": target_id, "name": new_name, "by": caller_id}
    if target_id != caller_id:
        out["note"] = "You renamed ANOTHER user - horizontal IDOR."
    return out, 200


def set_role(board_id, target_id, role, caller_id):
    """GraphQL updateMemberRole. VULN #3: role value trusted from the client.

    An admin may only grant 'member' - but nothing stops them sending
    role:"owner". The UI limits the dropdown; the server does not.
    """
    board = BOARDS.get(board_id)
    if not board or target_id not in USERS:
        return {"error": "not found"}, 404
    if board["members"].get(caller_id) not in ("admin", "owner"):
        return {"error": "forbidden"}, 403
    board["members"][target_id] = role  # no max-grantable-role check!
    out = {"board": board_id, "user": target_id, "role": role}
    if role == "owner":
        out["flag"] = FLAG_ROLE
        out["note"] = "Admin -> Owner by tampering the role value."
    return out, 200


def billing_page(board_id, caller_id):
    """Owner-only billing/transfer page."""
    board = BOARDS.get(board_id)
    if not board:
        return {"error": "not found"}, 404
    if board["members"].get(caller_id) != "owner":
        return {"error": "owner only"}, 403
    return {"board": board_id, "billing": board["billing"],
            "transfer": "ownership transfer available", "flag": FLAG_ROLE}, 200

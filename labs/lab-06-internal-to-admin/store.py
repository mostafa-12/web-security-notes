"""Lab-06 data layer: sessions, invitations, role grants.

The feature (inviting a user) has two endpoints with different privilege
surfaces. The admin one takes a role parameter the backend never validates
against the CALLER's role. That missing comparison is the whole bug.
"""
from config import FLAG, TOKENS

CREATED = []  # audit trail of granted invitations


def role_of(auth_header):
    """Map an Authorization header to a role (None = anonymous)."""
    return TOKENS.get((auth_header or "").replace("Bearer ", ""))


def invite_contact(requester_role, body):
    """Process POST /api/v1/contacts. Returns (payload, http_status).

    VULN: authenticates the caller but never asks "can THIS role grant
    THESE roles?" - the client-supplied companyUserRoles is trusted as-is.
    """
    wanted = body.get("companyUserRoles", ["user"])
    CREATED.append({"by": requester_role, "roles": wanted})
    out = {"status": "contact invited", "roles": wanted, "invitedBy": requester_role}
    if requester_role == "internal" and ("manager" in wanted or "administrator" in wanted):
        out["flag"] = FLAG
        out["note"] = "Internal User granted elevated role - privesc!"
    return out, 201

"""Lab-11 data layer: the role registry.

The endpoint authorizes from JWT scopes - dp.entitlements.plans.write.
That scope name covers PLANS, yet the same check gates ROLES. Two bugs
for the price of one: over-granted token + over-broad scope namespace.
"""
from config import FLAG

ROLES = [{"name": "viewer", "permissions": ["read"]}]


def create_role(claims, body):
    """POST /development/entitlements/roles. Needs plans.write scope."""
    if "dp.entitlements.plans.write" not in claims.get("scopes", []):
        return {"error": "missing scope"}, 403
    role = {"name": body.get("name", "unnamed"),
            "permissions": body.get("permissions", [])}
    ROLES.append(role)
    out = {"created": role, "by_role": claims.get("role")}
    if claims.get("role") == "Backoffice Editor":
        out["flag"] = FLAG
        out["note"] = "Editor created a role - the disabled UI was cosmetic."
    return out, 201

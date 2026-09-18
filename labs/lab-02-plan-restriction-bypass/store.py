"""Lab-02 data layer: the data-forwarding configuration store.

In a real app this would be a per-project row in Postgres. Here a dict.
The plan check that SHOULD gate writes lives... nowhere. That is the bug.
"""
from config import FLAG

FORWARDING = {"enabled": False, "instance": None, "index": None, "by": None}


def get_forwarding():
    return FORWARDING


def enable_forwarding(cfg, user):
    """Save a forwarding config. Returns the saved object (+flag for free users).

    VULN: no server-side plan check - a free-tier user can enable a paid
    feature. The dashboard hides the button, but hiding != enforcing.
    """
    FORWARDING.update({"enabled": True, "instance": cfg.get("instance"),
                       "index": cfg.get("index"), "by": user})
    out = dict(FORWARDING)
    if user == "free":
        out["flag"] = FLAG
        out["note"] = "Paid feature enabled from a FREE account."
    return out

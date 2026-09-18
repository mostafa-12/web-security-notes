"""Lab-04 data layer: two Algolia-style indexes + the query engine.

In a real app this would be Algolia/Elasticsearch. Here plain lists, with
the same query semantics the writeup abuses: attributesToRetrieve,
filters, facets, hitsPerPage.
"""
from config import FLAG

TALENT = [
    {"username": "talent_01", "name": "Talent One",
     "internal_engagement_scores": {"lifetime_completed_gmv": 98210},
     "computed_features_order_counts": 312,
     "restrictions": "high", "talent_demographic": {"gender": "female"}},
    {"username": "talent_02", "name": "Talent Two",
     "internal_engagement_scores": {"lifetime_completed_gmv": 1200},
     "computed_features_order_counts": 5,
     "restrictions": "none", "talent_demographic": {"gender": "male"}},
    {"username": "talent_03", "name": "Talent Three",
     "internal_engagement_scores": {"lifetime_completed_gmv": 55500},
     "computed_features_order_counts": 140,
     "restrictions": "high", "talent_demographic": {"gender": "non_binary"},
     "flag": FLAG},
]
BUSINESS = [{"company": f"biz_{i:03d}", "revenue": 1000 * i} for i in range(1, 81)]

INDEXES = {"prod_talent_v0": TALENT, "prod_business_talent_v0": BUSINESS}

# Fields the dashboard enables for filtering (attributesForFaceting).
# Anything else in `filters` is rejected - EXCEPT restrictions, which
# should never have been enabled. That misconfig is the oracle.
FILTERABLE = {"restrictions"}


def search(index, query):
    """Run an Algolia-style query. Returns (payload, http_status)."""
    data = INDEXES.get(index)
    if data is None:
        return {"message": "index not found"}, 404
    hits = list(data)
    if query.get("filters"):
        field, _, value = query["filters"].partition(":")
        if field not in FILTERABLE:
            return {"message": f"attribute '{field}' is not filterable"}, 400
        hits = [h for h in hits if h.get(field) == value]
    total = len(hits)
    if query.get("facets"):
        out = {}
        for facet in query["facets"]:
            if facet == "talent_demographic.gender":
                counts = {}
                for h in hits:
                    g = h.get("talent_demographic", {}).get("gender", "?")
                    counts[g] = counts.get(g, 0) + 1
                out[facet] = counts
        return {"nbHits": total, "facets": out}, 200
    per_page = int(query.get("hitsPerPage", 20))
    if per_page == 0:
        return {"nbHits": total, "hits": []}, 200  # volume probe
    attrs = query.get("attributesToRetrieve")  # None = all (the field dictionary)
    records = [h if attrs is None else {k: h.get(k) for k in attrs}
               for h in hits[:per_page]]
    return {"nbHits": total, "hits": records}, 200


def index_summary():
    return {"items": [{"name": k, "entries": len(v)} for k, v in INDEXES.items()]}

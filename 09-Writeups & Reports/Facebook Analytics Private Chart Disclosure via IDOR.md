# Case Study — Facebook Analytics Private Chart Disclosure via IDOR

> **Original write-up:** [Disclose Private Dashboard Chart's name and data in Facebook Analytics — Bugreader](https://bugreader.com/jubabaghdad@disclose-private-dashboard-charts-name-and-data-in-facebook-analytics-184)
> **Researcher:** Sarmad Hassan (jubabaghdad) — Published 07 May 2020
> **Target:** Facebook Analytics (`graph.facebook.com/graphql`) — custom dashboards
> **The one principle behind everything:** [[03-Web-Vulnerabilities/temp.md]] — two components interpreting the same data differently (here: *Dashboard query enforces Private/Owner-only* vs *Chart resolver trusts `chartID` alone*).

---

## TL;DR

Facebook Analytics lets you create custom dashboards and set visibility to **Private (Owner only)**. The Dashboard path enforced it correctly — an Analyst couldn't open the Admin's private dashboard. But the Chart path didn't: `AnalyticsChartDeleteMutation` with any victim `chartID` returned the chart's **title + full query spec + data definition** to any user with a role on the entity (e.g. Analyst). Reported 17 Feb 2020, triaged 26 Feb, fixed 08 Mar, bounty awarded 02 Apr. Severity: **LOW, VALID**.

---

## The Chain (foundation → application)

### 1) The feature — Private Dashboard
Custom dashboards = curated view of charts in one place. Visibility flag:
- Public
- **Private = only the owner sees it and its contents**

```
Dashboard (Private, owner=Admin)
 └─ Chart (title, chartType, chartQueries, dateRange, ...)
```

### 2) The two access paths (secure vs vulnerable)
Same data, two resolvers:

1. **Via parent (safe):** `dashboard(id) { charts { ... } }` → checks `dashboard.visibility + owner == requester`. Analyst blocked. ✓
2. **Direct child (vulnerable):** GraphQL mutation taking `chartID` alone → fetches chart row by ID, returns it with no owner/visibility check. ✗

> Technically independent objects in DB + GraphQL `node` model: the child has its own global ID and endpoint, so parent auth never runs.

### 3) Exploit shape (minimal)
```http
POST /graphql?locale=user HTTP/1.1
Host: graph.facebook.com

access_token=<ANALYST_TOKEN>
&fb_api_req_friendly_name=AnalyticsChartDeleteMutation
&doc_id=1297068037067230
&variables={"chartID":"<ADMIN_PRIVATE_CHART_ID>"}
```
Response (`200 OK`) leaks:
```json
{
  "data": {"node": {
    "__typename": "AnalyticsStoredAggregationChart",
    "title": "private chart name",
    "chartType": "BREAKDOWN_TABLE",
    "chartQueries": [{
      "aggregationMetric": "UNIQUE_USERS",
      "eventName": "fb_pages_post_reaction",
      "breakdowns": ["$fb.age"],
      "dateRange": {"type": "LAST_28_DAYS"}
    }]
  }}
}
```

> A *delete* mutation acting as a *read* oracle — it returns the node before/instead of deleting. Data leaks even if deletion never happens.

### 4) Why it happens
- **Wrong assumption:** "Child lives inside Private parent, so nobody can reach it." Forgets the direct child endpoint.
- **Resolver split:** Dashboard resolver has the check; Chart resolver does `get_chart_by_id(chartID)` with no `chart.dashboard.visibility + owner` check.
- **Frontend hiding ≠ security:** UI hides the dashboard from Analyst, but the `chartID` is replayable directly against the API.

### 5) The missing check
```python
# What the endpoint SHOULD do (pseudocode)
def resolve_chart(request):
    chart = lookup_by_chart_id(request.chartID)
    dashboard = lookup_dashboard(chart.dashboard_id)

    # MISSING (both of these):
    if dashboard.visibility == "private" and dashboard.owner != request.user:
        return 404  # don't reveal existence
    if not user_has_role_on_entity(request.user, dashboard.entity):
        return 404

    return chart
```

Fix = enforce visibility/ownership on **every** read of the child, not just the parent path.

---

## Concept Mapping

- **Vulnerability class:** **BOLA / IDOR** — `chartID` is the only guard, ownership/visibility never verified at read time.
  → [[03-Web-Vulnerabilities/Access control vulnerabilities/IDOR (Insecure Direct Object Reference).md|IDOR]]
- **Root cause:** *auth ≠ authz* on the consuming endpoint + missing inheritance of the Private flag to the child.
  → [[03-Web-Vulnerabilities/Methodology/Access Control Testing Methodology.md|Access Control Testing Methodology]]
- **Sibling pattern in this repo:** exact same Parent→Child shape as [[09-Writeups & Reports/Gmail API Attachment IDOR - Missing Object-Level Authorization]] (`Message → Attachment` = `Dashboard → Chart`) and [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]] (issuing endpoint correct, redeeming endpoint forgotten).
- **Scope lesson:** requires a role on the entity (Analyst) + victim `chartID` — caps severity to LOW, but breaks the Owner-only promise.

---

## New Techniques

> Skills in this write-up the repo doesn't document explicitly yet.

1. **"Sub-option" audit** — when a feature has Main (Dashboard visibility) + Sub (Chart info), test authz on the Sub independently. Devs protect the Main and forget the Sub.
2. **Mutations as read oracles** — `Delete/Update` mutations often echo the full object back. A forbidden delete can still be a successful read. Always read the returned `node`.
3. **Parent-path vs direct-node diff** — for any nested object, query it both ways: nested under parent vs direct by global ID (`node(id)` / `doc_id` + `chartID`). Different auth = finding.

---

## Key Takeaways

1. **Authorization must run on every level** — child objects don't inherit parent checks automatically. Each resolver needs `owner == requester`.
2. **Logical IDOR lives in Sub-options** — Private/Public, Owner-only, Hidden tabs: every sub-setting is a new endpoint to test.
3. **Delete ≠ only delete** — GraphQL mutations returning the object turn a write endpoint into a disclosure primitive.
4. **Low-priv + victim ID = valid LOW** — needing Analyst role + chartID caps impact, but still breaks confidentiality. Don't skip it.

---

## References

- [Disclose Private Dashboard Chart's name and data in Facebook Analytics — Bugreader](https://bugreader.com/jubabaghdad@disclose-private-dashboard-charts-name-and-data-in-facebook-analytics-184)
- Sibling case: [[09-Writeups & Reports/Gmail API Attachment IDOR - Missing Object-Level Authorization]]
- Sibling case: [[09-Writeups & Reports/IDOR + Public S3 Report Exposure]]
- Summary row + Q&A: [[09-Writeups & Reports/Reports Summary Table]]
- Core principle: [[03-Web-Vulnerabilities/temp.md]]

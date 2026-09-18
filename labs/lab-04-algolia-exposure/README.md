# Lab-04 — Algolia Search Key Over-Exposure (simulation)

**Recreates:** `Algolia Search Key Over-Exposure - 154k Records.md`
**Run:** `python app.py` → `http://127.0.0.1:8004`
**Setup (once):** `python -m pip install -r ../requirements.txt` from the `labs/` folder.

## Scenario
A public search key leaked in a JS bundle. The key itself is public by design — the bug is its **permissions**: it returns internal financial fields, filters by moderation status, reaches a second index, and exposes sensitive facets. Plus a leaked `server.js.map`.

## Your goal (no login)
1. Extract `appId` + `apiKey` + `indexName` from the bundle.
2. Run a wildcard query and discover the internal field names.
3. Request the internal fields by name + filter `restrictions:high` + gender facets + `hitsPerPage:0` on the second index.
4. Grab the flag from a record + find the dev key in the source map.

## Starting points
- `GET /dist/bundle-abc123.js`, then `grep apiKey`
- `POST /1/indexes/<index>/query` with `X-Algolia-Application-Id` and `X-Algolia-API-Key` headers

## Success criteria
- A response containing `internal_engagement_scores` + `FLAG{...}`, and `GET /1/indexes` listing the second index.

## Hints
<details><summary>Hint 1</summary>Drop attributesToRetrieve entirely — the default returns all fields. The raw JSON is the field dictionary.</details>
<details><summary>Hint 2</summary>Try filters="restrictions:high". A non-filterable field returns "attribute is not filterable".</details>
<details><summary>Hint 3</summary>hitsPerPage:0 counts records without downloading them. And try GET /1/indexes with the same key.</details>
<details><summary>Hint 4</summary>Append .map to dist paths and see what returns 200.</details>

Solution in `SOLUTION.md`.

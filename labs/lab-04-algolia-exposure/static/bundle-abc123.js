// production bundle
const algoliaConfig = { appId:"LABAPP123", apiKey:"search-public-key-lives-in-js", talentIndexName:"prod_talent_v0" };
function search(q){ return fetch("/1/indexes/prod_talent_v0/query",{method:"POST"}); }

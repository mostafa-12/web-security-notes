// Sentry-like SPA bundle
const routes = ["/settings/projects/PROJECT_SLUG/plugins/splunk/",
  "/settings/projects/PROJECT_SLUG/plugins/slack/"];
function saveSplunk(org,project,cfg){ return fetch("/api/0/projects/"+org+"/"+project+"/plugins/splunk/",{method:"PUT",body:JSON.stringify(cfg)}); }

// Backbone view for users page (ADMIN - do not expose)
function addNewUser(){ return fetch("Users.aspx/manageUserProfile", {method:"POST"}); }
// admin endpoint: /app/region/east/Users.aspx/manageUserProfile?userId=1001

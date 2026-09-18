// Backbone view for courses page
var CoursesView = Backbone.View.extend({ el: "#courses" });
// views/ names mirror .aspx names, e.g. views/courses/index.js <-> courses.aspx
function listCourses(){ return fetch("/app/region/east/courses.aspx"); }

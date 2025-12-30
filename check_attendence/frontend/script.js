function loadEmployees() {
 fetch("http://127.0.0.1:8000/employees")
 .then(r => r.json())
 .then(d => document.getElementById("output").innerText = JSON.stringify(d,null,2));
}

function loadAttendance() {
 fetch("http://127.0.0.1:8000/attendance")
 .then(r => r.json())
 .then(d => document.getElementById("output").innerText = JSON.stringify(d,null,2));
}

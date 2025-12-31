const API = "http://127.0.0.1:5000";

function clearTable() {
    document.querySelector("thead").innerHTML = "";
    document.querySelector("tbody").innerHTML = "";
}

function loadStudents() {
    fetch(`${API}/admin/students`)
        .then(res => res.json())
        .then(data => {
            clearTable();

            const thead = document.querySelector("thead");
            thead.innerHTML = "<tr><th>Roll No</th><th>Name</th></tr>";

            const tbody = document.querySelector("tbody");
            data.forEach(row => {
                tbody.innerHTML += `
                    <tr>
                        <td>${row[0]}</td>
                        <td>${row[1]}</td>
                    </tr>`;
            });
        });
}

function loadAttendance() {
    fetch(`${API}/admin/attendance`)
        .then(res => res.json())
        .then(data => {
            clearTable();

            const thead = document.querySelector("thead");
            thead.innerHTML = "<tr><th>Roll No</th><th>Date</th><th>Time</th></tr>";

            const tbody = document.querySelector("tbody");
            data.forEach(row => {
                tbody.innerHTML += `
                    <tr>
                        <td>${row[0]}</td>
                        <td>${row[1]}</td>
                        <td>${row[2]}</td>
                    </tr>`;
            });
        });
}

function exportAttendance() {
    window.location.href = `${API}/admin/export`;
}

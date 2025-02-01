import { apiRequest } from "/scripts/api.js";

async function loadVacationRequests() {
    // Fetch vacation requests for the authenticated employee (from /vacation_requests/me)
    const requests = await apiRequest("/vacation_requests/me");

    const tableBody = document.getElementById("vacation-requests-table");
    tableBody.innerHTML = ""; // Clear table before repopulating

    requests.forEach(request => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${request.start_date}</td>
            <td>${request.end_date}</td>
            <td>${request.reason}</td>
            <td>${request.status}</td>
            <td>${request.reviewed_by ? request.reviewed_by : 'Not Reviewed'}</td>
        `;

        tableBody.appendChild(row);
    });
}

// Load vacation requests when the page loads
loadVacationRequests();

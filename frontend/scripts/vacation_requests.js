import { apiRequest } from "/scripts/api.js";

async function loadVacationRequests() {
    // Fetch all vacation requests for the manager (from /vacation_requests)
    const requests = await apiRequest("/vacation_requests");

    const tableBody = document.getElementById("vacation-requests-table");
    tableBody.innerHTML = ""; // Clear table before repopulating

    requests.forEach(request => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${request.employee_name}</td>
            <td>${request.employee_code}</td>
            <td>${request.start_date}</td>
            <td>${request.end_date}</td>
            <td>${request.reason}</td>
            <td>${request.status}</td>
            <td>${request.reviewed_by ? request.reviewed_by : 'Not Reviewed'}</td>
            <td>
                <button class="approve-btn" data-request-id="${request.id}">Approve</button>
                <button class="reject-btn" data-request-id="${request.id}">Reject</button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

// Load vacation requests when the page loads
loadVacationRequests();

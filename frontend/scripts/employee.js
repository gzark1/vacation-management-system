import { apiRequest } from "/scripts/api.js";

async function loadVacationRequests() {
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
            <td>${request.reviewed_by || 'Not Reviewed'}</td>
            <td>
                ${request.status === 'pending' ? `<button class="delete-btn" data-request-id="${request.id}">Delete</button>` : ''}
            </td>
        `;

        tableBody.appendChild(row);
    });

    // Handle delete action
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener("click", async () => {
            const request_id = btn.dataset.requestId;
            await deleteRequest(request_id);
        });
    });
}

async function deleteRequest(request_id) {
    const response = await apiRequest(`/vacation_requests/${request_id}`, "DELETE");

    if (response.error) {
        alert("Error deleting request: " + response.error);
    } else {
        alert("Vacation request deleted successfully!");
        loadVacationRequests();  // Reload requests
    }
}

loadVacationRequests();

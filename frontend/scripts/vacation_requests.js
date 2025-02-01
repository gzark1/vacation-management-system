import { apiRequest } from "/scripts/api.js";

async function loadVacationRequests() {
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
            <td>${request.reviewed_by || 'Not Reviewed'}</td>
            <td>
                ${request.status === "pending" ? `
                    <button class="approve-btn" data-request-id="${request.id}">Approve</button>
                    <button class="reject-btn" data-request-id="${request.id}">Reject</button>
                ` : ''}
            </td>
        `;

        tableBody.appendChild(row);
    });

    // Handle approve/reject actions
    document.querySelectorAll('.approve-btn').forEach(btn => {
        btn.addEventListener("click", async () => {
            const request_id = btn.dataset.requestId;
            await reviewRequest(request_id, "approved");
        });
    });

    document.querySelectorAll('.reject-btn').forEach(btn => {
        btn.addEventListener("click", async () => {
            const request_id = btn.dataset.requestId;
            await reviewRequest(request_id, "rejected");
        });
    });
}

async function reviewRequest(request_id, status) {
    const response = await apiRequest(`/vacation_requests/${request_id}/review`, "POST", { status });

    if (response.error) {
        alert("Error updating request: " + response.error);
    } else {
        alert(`Vacation request ${status} successfully!`);
        loadVacationRequests();  // Refresh the list
    }
}

loadVacationRequests();

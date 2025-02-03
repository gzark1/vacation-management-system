import { apiRequest } from "/scripts/api.js";

// Function to load and display all vacation requests (Manager only)
async function loadVacationRequests() {
    // Fetch vacation requests from the API
    const requests = await apiRequest("/vacation_requests");

    // Select the table body and clear previous data
    const tableBody = document.getElementById("vacation-requests-table");
    tableBody.innerHTML = ""; // Reset table before repopulating

    // Loop through each request and create a row in the table
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

    // Attach event listeners to approve buttons
    document.querySelectorAll('.approve-btn').forEach(btn => {
        btn.addEventListener("click", async () => {
            const request_id = btn.dataset.requestId;
            await reviewRequest(request_id, "approved");
        });
    });

    // Attach event listeners to reject buttons
    document.querySelectorAll('.reject-btn').forEach(btn => {
        btn.addEventListener("click", async () => {
            const request_id = btn.dataset.requestId;
            await reviewRequest(request_id, "rejected");
        });
    });
}

// Function to approve or reject a vacation request
async function reviewRequest(request_id, status) {
    // Send API request to update the vacation request status
    const response = await apiRequest(`/vacation_requests/${request_id}/review`, "POST", { status });

    if (response.error) {
        alert("Error updating request: " + response.error);
    } else {
        alert(`Vacation request ${status} successfully!`);
        loadVacationRequests();  // Refresh the request list
    }
}

// Load vacation requests when the page loads
loadVacationRequests();

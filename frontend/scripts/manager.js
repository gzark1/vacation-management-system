import { apiRequest } from "./api.js";

// Function to load all users (Manager only)
async function loadUsers() {
    const users = await apiRequest("/users");
    
    const usersTable = document.getElementById("users-table");
    usersTable.innerHTML = ""; // Clear table before repopulating

    users.forEach(user => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>
                <button class="edit-btn" data-user-id="${user.id}">Edit</button>
                <button class="delete-btn" data-user-id="${user.id}">Delete</button>
            </td>
        `;

        usersTable.appendChild(row);
    });
}

// Function to delete a user
async function deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    const response = await apiRequest(`/users/${userId}`, "DELETE");

    if (response.error) {
        alert("Error deleting user: " + response.error);
    } else {
        alert("User deleted successfully!");
        loadUsers();  // Refresh list after deletion
    }
}

// Attach delete event listener to buttons
document.getElementById("users-table").addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-btn")) {
        const userId = event.target.dataset.userId;
        deleteUser(userId);
    }
    
    if (event.target.classList.contains("edit-btn")) {
        const userId = event.target.dataset.userId;
        window.location.href = `/public/user_form.html?id=${userId}`;
    }
});

// Attach event listener to create user button
document.getElementById("create-user").addEventListener("click", () => {
    window.location.href = "/public/user_form.html"; // Redirect to the user form for creating a new user
});

// Load users when the page loads
loadUsers();

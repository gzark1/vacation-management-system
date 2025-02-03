import { apiRequest } from "./api.js";

// Get query parameters from the URL (used for editing a user)
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get("id");  // Extract user ID if editing an existing user

document.addEventListener("DOMContentLoaded", async () => {
    if (userId) {
        // If editing an existing user, update form title and hide fields that shouldn't be changed
        document.getElementById("form-title").innerText = "Edit User";
        document.getElementById("employee_code").style.display = "none";
        document.getElementById("employee-code-label").style.display = "none";
        document.getElementById("role").style.display = "none";
        document.getElementById("role-label").style.display = "none";

        // Fetch user data and populate form fields
        const user = await apiRequest(`/users/${userId}`);
        document.getElementById("name").value = user.name;
        document.getElementById("email").value = user.email;
    }
});

// Handle form submission for both creating and updating users
document.getElementById('submit-button').addEventListener('click', async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    // Collect form input values
    const userData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
    };

    if (!userId) {
        // If creating a new user, gather additional required fields
        userData.employee_code = document.getElementById("employee_code").value;
        if (!/^\d{7}$/.test(userData.employee_code)) {
            alert("Employee code must be exactly 7 digits.");
            return;
        }
        userData.password = document.getElementById("password").value;
        userData.role = document.getElementById("role").value;
    
        // Send API request to create the user
        await apiRequest("/users", "POST", userData);
        alert("User created successfully!");
    } else {
        // If editing an existing user, update the provided fields
        if (document.getElementById("password").value) {
            userData.password = document.getElementById("password").value;
        }

        console.log(userData);
        await apiRequest(`/users/${userId}`, "PUT", userData);
        alert("User updated successfully!");
    }

    // Redirect back to the manager's dashboard after action is completed
    window.location.href = "/public/manager.html";
});

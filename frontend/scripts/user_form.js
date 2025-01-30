import { apiRequest } from "./api.js";

const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get("id");  // Get user ID from URL if editing

document.addEventListener("DOMContentLoaded", async () => {
    if (userId) {
        // Editing user - Fetch user data and prefill form
        document.getElementById("form-title").innerText = "Edit User";
        document.getElementById("employee_code").style.display = "none";
        document.getElementById("employee-code-label").style.display = "none";
        document.getElementById("role").style.display = "none";
        document.getElementById("role-label").style.display = "none";

        const user = await apiRequest(`/users/${userId}`);
        document.getElementById("name").value = user.name;
        document.getElementById("email").value = user.email;
    }
});


document.getElementById('submit-button').addEventListener('click', async (event) => {
    event.preventDefault();

    const userData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
    };

    if (!userId) {
        // Creating a new user
        userData.employee_code = document.getElementById("employee_code").value;
        userData.password = document.getElementById("password").value;
        userData.role = document.getElementById("role").value;
    
        await apiRequest("/users", "POST", userData);
        alert("User created successfully!");
    } else {
        // Editing an existing user
        if (document.getElementById("password").value) {
            userData.password = document.getElementById("password").value;
        }
        console.log(userData);
        await apiRequest(`/users/${userId}`, "PUT", userData);
        alert("User updated successfully!");
    }

    window.location.href = "/public/manager.html";
});
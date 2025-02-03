// Fetch the navbar HTML from the public directory and insert it into the page
fetch('/public/navbar.html')
    .then(response => response.text())  // Get the response as text
    .then(html => {
        document.getElementById('navbar-container').innerHTML = html; // Insert navbar HTML

        // Retrieve the authentication token from localStorage
        const token = localStorage.getItem("token");
        if (!token) return;  // If no token is found, skip modifying the navbar

        try {
            // Decode JWT token to extract user role
            const payload = JSON.parse(atob(token.split(".")[1]));
            const userRole = payload.role;
            const roleLinksContainer = document.getElementById("role-specific-links");

            // Display links based on the user's role
            if (userRole === "manager") {
                roleLinksContainer.innerHTML = `
                    <a href="/public/manager.html">Manage Users</a>
                    <a href="/public/vacation_requests.html">Vacation Requests</a>
                `;
            } else if (userRole === "employee") {
                roleLinksContainer.innerHTML = `
                    <a href="/public/employee.html">My Vacation Requests</a>
                `;
            }
        } catch (error) {
            console.error("Invalid token:", error);
            localStorage.removeItem("token");  // Clear invalid token
            window.location.href = "/public/index.html";  // Redirect to login page
        }

        // Attach event listener for logout button
        document.getElementById("logout-button").addEventListener("click", function () {
            localStorage.removeItem("token");  // Remove token from local storage
            window.location.href = "/public/index.html";  // Redirect to login page
        });
    });

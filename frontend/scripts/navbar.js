fetch('/public/navbar.html')
.then(response => response.text())
.then(html => {
    document.getElementById('navbar-container').innerHTML = html;

    // After loading the navbar, modify it based on role
    const token = localStorage.getItem("token");
    if (!token) return;  // No token = don't modify anything

    try {
        const payload = JSON.parse(atob(token.split(".")[1]));  // Decode JWT
        const userRole = payload.role;
        const roleLinksContainer = document.getElementById("role-specific-links");

        if (userRole === "manager") {
            roleLinksContainer.innerHTML = `
                <a href="/public/manager.html">Manage Users</a>
                <a href="/public/vacation_requests.html">Vacation Requests</a> <!-- Correct path now -->
            `;
        } else if (userRole === "employee") {
            roleLinksContainer.innerHTML = `
                <a href="/public/employee.html">My Vacation Requests</a>
            `;
        }
    } catch (error) {
        console.error("Invalid token:", error);
        localStorage.removeItem("token");  // Clear invalid token
        window.location.href = "/public/index.html";  // Redirect to login
    }

    // Attach logout functionality
    document.getElementById("logout-button").addEventListener("click", function () {
        localStorage.removeItem("token");  // Remove JWT
        window.location.href = "/public/index.html";  // Redirect to login
    });
});

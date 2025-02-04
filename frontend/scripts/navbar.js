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
                    <a href="/public/manager.html" class="navbar-link">Manage Users</a>
                    <a href="/public/vacation_requests.html" class="navbar-link">Vacation Requests</a>
                    <a href="#" class="navbar-link under-construction-link">Audit Logs</a>
                `;
            } else if (userRole === "employee") {
                roleLinksContainer.innerHTML = `
                    <a href="/public/employee.html" class="navbar-link">My Vacation Requests</a>
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

        // Handle "Under Construction" links
        const underConstructionLinks = document.querySelectorAll('.under-construction-link');
        const modal = document.getElementById("construction-modal");
        const closeBtn = document.querySelector(".close");

        underConstructionLinks.forEach(link => {
            link.addEventListener("click", (event) => {
                event.preventDefault();  // Prevent navigation
                modal.style.display = "block"; // Show the modal
            });
        });

        // Close modal when clicking the "X" button
        closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });

        // Close modal when clicking outside the modal content
        window.addEventListener("click", (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });

        // 🎯 Set Active Class for Current Page
        const currentPath = window.location.pathname; // Get current page path
        console.log(currentPath);
        document.querySelectorAll(".navbar-link").forEach(link => {
            if (link.getAttribute("href") === currentPath) {
                link.classList.add("active"); // Add active class to the matching link
            }
        });
    });

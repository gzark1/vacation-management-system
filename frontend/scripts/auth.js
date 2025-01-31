// Handle login form submission
document.getElementById("login-form")?.addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:8080/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const result = await response.json();
            throw new Error(result.error || "An error occurred");
        }

        const result = await response.json();
        localStorage.setItem("token", result.token); // Store JWT in localStorage

        redirectUser(result.role);
    } catch (error) {
        alert(error.message);
    }
});

// Redirect user based on role
function redirectUser(role) {
    console.log(`🔍 Redirecting user based on role: ${role}`);

    if (role === "manager") {
        window.location.href = "/public/manager.html";
    } else if (role === "employee") {
        window.location.href = "/public/employee.html";
    } else {
        console.warn("❌ Unknown role. Redirecting to index.");
        window.location.href = "/public/index.html";
    }
}

// Function to check authentication and restrict page access
function checkAuth(requiredRole = null) {
    console.log("🔐 Checking authentication...");
    const token = localStorage.getItem("token");

    if (!token) {
        console.warn("❌ No token found. Redirecting to error page.");
        window.location.href = "/public/error.html?msg=not_logged_in";
        return;
    }

    try {
        const payload = JSON.parse(atob(token.split(".")[1])); // Decode JWT payload
        const userRole = payload.role;
        console.log(`🔍 Auth Check: User Role: ${userRole}, Required Role: ${requiredRole}`);

        if (requiredRole && userRole !== requiredRole) {
            console.warn(`❌ Unauthorized access. Expected role: ${requiredRole}, but got: ${userRole}`);
            window.location.href = `/public/error.html?msg=unauthorized&role=${userRole}&required=${requiredRole}`;
            return;
        }
    } catch (error) {
        console.error("❌ Invalid token:", error);
        localStorage.removeItem("token");
        window.location.href = "/public/error.html?msg=invalid_token";
    }

}

// if no index.html, check authentication
if (!window.location.pathname.endsWith("index.html")) {
    // Get the script element
    const scriptTag = document.querySelector('script[src="/scripts/auth.js"]');

    // Access the data attribute
    const role = scriptTag.getAttribute('role');
    checkAuth(role);
}

// Function to log out the user
function logout() {
    localStorage.removeItem("token"); // Remove token from storage
    window.location.href = "/public/index.html"; // Redirect to login
}

// Attach logout event to button
document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logout-button");
    if (logoutButton) {
        logoutButton.addEventListener("click", logout);
    }
});

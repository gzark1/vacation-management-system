const API_BASE_URL = "http://localhost:8080";

/**
 * Generic function to make API requests.
 *
 * @param {string} endpoint - The API endpoint (e.g., "/users").
 * @param {string} [method="GET"] - The HTTP method (GET, POST, PUT, DELETE).
 * @param {Object|null} [body=null] - The request payload (if applicable).
 * @param {Object} [customHeaders={}] - Additional headers if needed.
 * @returns {Promise<Object|null>} - The JSON response from the API or `null` if no content.
 */
async function apiRequest(endpoint, method = "GET", body = null, customHeaders = {}) {
    const token = localStorage.getItem("token");

    // 🚨 Redirect to error page if there's NO token (except for index.html)
    if (!token) {
        console.warn("No token found. Redirecting to error page.");
        window.location.href = "/public/error.html?msg=not_logged_in";
        return null;
    }

    const headers = { "Content-Type": "application/json", ...customHeaders };
    headers["Authorization"] = `Bearer ${token}`;

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        console.log(`API Request: ${method} ${endpoint}`);
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        // Handle non-2xx responses explicitly
        if (!response.ok) {
            const errorResponse = await response.json();
            console.error("API Error:", errorResponse);
            
            // 🚨 Handle unauthorized errors (invalid token, expired token)
            if (response.status === 401 || response.status === 403) {
                console.warn("Unauthorized access. Redirecting to error page.");
                window.location.href = "/public/error.html?msg=unauthorized";
                return null;
            }

            throw new Error(errorResponse.error || `HTTP ${response.status}`);
        }

        return response.status !== 204 ? await response.json() : null;
    } catch (error) {
        console.error(`API Request failed: ${error.message}`);
        return { error: error.message };
    }
}

export { apiRequest };
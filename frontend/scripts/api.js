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
    console.log("changes to API");

    const token = localStorage.getItem("token");
    const headers = { "Content-Type": "application/json", ...customHeaders };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        // Handle non-2xx responses explicitly
        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || `HTTP ${response.status}`);
        }

        // Return JSON if response has content
        return response.status !== 204 ? await response.json() : null;
    } catch (error) {
        console.error(`API Request failed: ${error.message}`);
        return { error: error.message };
    }
}

export { apiRequest };

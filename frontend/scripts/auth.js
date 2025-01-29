document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Debug
    console.log(email);

    try {
        const response = await fetch("http://localhost:8080/login", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const result = await response.json();
            throw new Error(result.error || 'An error occurred');
        }

        const result = await response.json();
        console.log(result);
        localStorage.setItem("token", result.token);
        console.log(localStorage.getItem("token"));


        redirectUser(result.role);

    } catch (error) {
        alert(error.message);
    }
});

function redirectUser(role) {
    if (role === "manager") {
        window.location.href = "/public/manager.html";
    } else {
        window.location.href = "/public/employee.html";
    }
}
async function fetchUsers() {
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "/public/index.html";  // Redirect to login if no token
        return;
    }

    const response = await fetch("http://localhost:8080/users", {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const users = await response.json();

    if (response.ok) {
        const usersList = document.getElementById("users-list");
        users.forEach(user => {
            const li = document.createElement("li");
            li.textContent = `${user.name} (${user.role})`;
            usersList.appendChild(li);
        });
    } else {
        alert("Error fetching users");
    }
}

fetchUsers();

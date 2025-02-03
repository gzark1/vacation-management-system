# Vacation Portal

A full-stack vacation management system where **managers** can manage users and vacation requests, while **employees** can request and manage their own vacation requests.

## Key Features

### 1. **Manager Account:**
   - **Login and Logout:** Managers can sign in using their username and password to access the manager homepage, and sign out when finished.
   - **User Management:**
     - View a list of all users (employees and other managers).
     - Create new users by entering their name, email, employee code, and role (Employee or Manager).
     - Update user details, such as name, email, and password.
     - Delete users and ensure their associated data is also removed from the system.
   - **Vacation Request Management:**
     - Managers can view all vacation requests submitted by employees.
     - Approve or reject vacation requests based on the request details.
     - Each request is updated with its status (approved/rejected) upon review.

### 2. **Employee Account:**
   - **Login and Logout:** Employees can sign in to access their dashboard, and sign out when done.
   - **Vacation Request Management:**
     - Employees can view a list of their submitted vacation requests, including the status (pending, approved, or rejected), start date, end date, and reason for the vacation.
     - Employees can create new vacation requests by selecting the date range and entering a reason.
     - Employees can delete vacation requests that are still pending approval.
   - **Personal Dashboard:** Employees are presented with a personalized dashboard that allows them to manage their vacation requests efficiently, without seeing other employees' requests.

### 3. **Responsive and User-Friendly Interface:**
   - **Role-Based Navigation:** The navbar adjusts based on the user's role (Manager or Employee), displaying the appropriate links for user management, vacation requests, and logout.
   - **Mobile-Responsive Design:** The entire application is designed to be responsive, ensuring a good experience across all devices.
   - **Interactive UI:** Users can easily interact with tables, buttons, and forms for a seamless experience.

### 4. **Backend and Database:**
   - **Database Integration:** PostgreSQL is used as the backend database, ensuring secure and efficient storage of user and vacation request data.
   - **API:** The backend exposes RESTful APIs for user authentication, vacation request management, and user management.
   - **Secure Authentication:** JWT tokens are used for user authentication, ensuring secure access to the application.
   - **Role-Based Access:** Managers have additional permissions to manage users and approve/reject vacation requests, while employees can only manage their own requests.
   - **Password Hashing:** Passwords are securely hashed before storage, ensuring that no  passwords are saved in the database.

### 5. **Dockerized Application:**
   - The entire application is **dockerized** for easy setup and deployment. It consists of **3 containers**:
     - **PostgreSQL Database** (`vacation_db`).
     - **Backend** (`vacation_backend`) – running on port **8080**.
     - **Frontend** (`vacation_frontend`) – running on port **3000**.
   - The containers use **volumes** to persist data, including the database data, which ensures that the database contents are not lost between restarts.
   - **Integrated tests** run automatically when using `docker-compose up` to set up the application.
   - **Role-based access control** ensures that managers cannot access employee-only pages, and employees cannot access manager-only pages.
   - The application is built using **Werkzeug**, a Python library for routing and handling HTTP requests, rather than a full framework.

## Setup and Installation

### 1. Clone the repository:
```
git clone https://github.com/gzark1/vacation-management-system.git
cd vacation-management-system
```

2. Create .env files:
Make sure you have the following .env file in the backend directory (backend/.env):

```
DB_NAME=vacation_portal
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432
SECRET_KEY=my_secret_key
```

3. Build and start the containers:
Run the following command to build the Docker containers and start the services:


```
docker compose up --build
```

This will start the following three containers:

PostgreSQL Database (vacation_db) running on port 5433. <br>
Backend (vacation_backend) running on port 8080. <br>
Frontend (vacation_frontend) running on port 3000. <br>

4. Accessing the Application:
Frontend: Open http://localhost:3000 in your browser.
Backend: The API is accessible at http://localhost:8080.

5. Stopping the containers:

To stop the application, run the following:
```
docker compose down
```

## Folder Structure

```
├── backend/
│   ├── api/
│   ├── core/
│   ├── database/
|   ├── tests/
│   └── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── scripts/
│   └── styles/
│   └── Dockerfile
├── docker-compose.yml
└── README.md

```

* backend/: Contains the backend code and configurations.
* frontend/: Contains the frontend code.
* docker-compose.yml: Docker configurations to run the services.

## Environment Variables

<p>
The application requires the following environment variables (set in .env):

DB_USER: Database username

DB_PASSWORD: Database password

DB_NAME: Database name

But you can also use the ones set in ```docker-compose.yml```
</p>

## Usage

Once the application is running, you can access the frontend UI at http://localhost:3000.


## API Endpoints

### Detailed Explanation:

* #### Auth:

    * /login: POST request for logging in, either as an employee or a manager.
    * /logout: POST request to log out the current user.

* #### Users (Manager-only routes):

    * /users: GET to fetch a list of all users in the system, POST to create a new user.
    * /users/<int:user_id>: PUT to update a user's details, DELETE to remove a user.
    * /users/<int:user_id>: GET to fetch specific details about a user.

* #### Vacation Requests:

    * /vacation_requests: GET to fetch all vacation requests for managers (employees only see their own).
    * /vacation_requests/me: GET for employees to view only their own vacation requests.
    * /vacation_requests: POST for employees to create a new vacation request.
    * /vacation_requests/<int:request_id>/review: POST for managers to approve/reject vacation requests.
    * /vacation_requests/<int:request_id>: DELETE for employees to delete their own pending vacation requests.

## Testing

Integrated tests are run automatically when you run docker-compose up --build. You can also run unit tests for the backend separately using pytest.

## Sample Data and Login Details:
For development purposes, you can log in with a sample user from the database. The passwords are hashed, so you cannot directly see them. For test purposes, the password for each user is exactly the same as their name.

<p>
Example Login:

Email: manager@example.com

Password: Admin Manager

Email: alice@example.com

Password: Alice Employee

These credentials can be used to log in as an employee or manager.
</p>

## Contributing
Feel free to fork this repository and submit pull requests. We welcome any contributions to improve the application.
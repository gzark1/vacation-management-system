-- Users Table: Stores employees & managers
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    employee_code CHAR(7) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- Hashed password (bcrypt recommended)
    role VARCHAR(10) CHECK (role IN ('manager', 'employee')) NOT NULL,
    created_by INT REFERENCES users(id) ON DELETE SET NULL, -- Tracks who created this user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vacation Requests Table: Stores employee vacation requests
CREATE TABLE vacation_requests (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Employee who requested. If employee is deleted, their requests should be deleted
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status VARCHAR(10) CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    reviewed_by INT REFERENCES users(id) ON DELETE SET NULL, -- Tracks who approved/rejected request
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs Table (Optional): Tracks actions like user creation, vacation approvals
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(255) NOT NULL, -- e.g., "Created User", "Approved Vacation"
    details TEXT, -- Additional info
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
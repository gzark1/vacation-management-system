-- 
-- Database schema for the Vacation Management System
-- Defines tables for user accounts, vacation requests, and audit logs (under development).
--

-- =============================================
-- Users Table: Stores employees & managers
-- =============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Unique identifier for each user
    name VARCHAR(100) NOT NULL,  -- Full name of the user
    email VARCHAR(100) UNIQUE NOT NULL,  -- Unique email address for login
    employee_code CHAR(7) UNIQUE NOT NULL,  -- Unique employee identifier
    password_hash TEXT NOT NULL,  -- Hashed password (bcrypt recommended for security)
    role VARCHAR(10) CHECK (role IN ('manager', 'employee')) NOT NULL,  -- Defines role-based access (Manager or Employee)
    created_by INT REFERENCES users(id) ON DELETE SET NULL,  -- Tracks who created this user (Nullable if creator is removed)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp for user creation
);

-- =============================================
-- Vacation Requests Table: Stores employee vacation requests
-- =============================================
CREATE TABLE vacation_requests (
    id SERIAL PRIMARY KEY,  -- Unique identifier for each vacation request
    employee_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- Employee making the request (Deletes requests if employee is removed)
    start_date DATE NOT NULL,  -- Vacation start date
    end_date DATE NOT NULL,  -- Vacation end date
    reason TEXT,  -- Reason for the vacation (optional)
    status VARCHAR(10) CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',  -- Request status
    reviewed_by INT REFERENCES users(id) ON DELETE SET NULL,  -- Tracks who approved/rejected the request (Nullable)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp for request submission
);

-- =============================================
-- Audit Logs Table (Not in Use)
-- =============================================
-- This table is intended to track system actions (e.g., user creation, approvals).
-- It is currently under development and not in use.

-- CREATE TABLE audit_logs (
--     id SERIAL PRIMARY KEY,  -- Unique identifier for each log entry
--     user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- User performing the action (Deletes logs if user is removed)
--     action VARCHAR(255) NOT NULL,  -- Description of the action (e.g., "Created User", "Approved Vacation")
--     details TEXT,  -- Additional information related to the action
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp of when the action occurred
-- );

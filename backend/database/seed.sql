-- Ensure tables exist (use schema.sql for structure)

-- Insert default manager user
INSERT INTO users (name, email, employee_code, password_hash, role, created_by) VALUES
('Admin Manager', 'manager@example.com', '0000001', '$2b$12$a23A0i0PN8VYyx0//UNUl.f2lNI1yzJjR0zv0AIiWcdFAhN3XlC9O', 'manager', NULL),
('Alice Employee', 'alice@example.com', '1234567', '$2b$12$I4UWyiycfxUO0m.3FZil3uPMmQEEUkiJ1z8HEWTNBthymNhGWl9h2', 'employee', 1),
('Bob Employee', 'bob@example.com', '7654321', '$2b$12$ZSIHkay6L6YMmTtQFbY7je3dHMysmfOR2lTmw5JoFqsR9R3AWJL9W', 'employee', 1);

-- Insert sample vacation requests
INSERT INTO vacation_requests (employee_id, start_date, end_date, reason, status, reviewed_by) VALUES
(2, '2024-07-01', '2024-07-10', 'Family trip', 'pending', NULL),
(3, '2024-08-15', '2024-08-20', 'Medical leave', 'approved', 1),
(2, '2024-09-10', '2024-09-15', 'Personal time', 'rejected', 1);

-- Insert sample audit logs
INSERT INTO audit_logs (user_id, action, details) VALUES
(1, 'Created User', 'Alice Employee was added to the system.'),
(1, 'Created User', 'Bob Employee was added to the system.'),
(1, 'Approved Vacation', 'Approved vacation request for Bob Employee.');

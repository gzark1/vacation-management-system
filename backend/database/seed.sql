-- Insert default users
INSERT INTO users (name, email, employee_code, password_hash, role, created_by) VALUES
('Admin Manager', 'manager@example.com', '0000001', '$2b$12$ANdshZnhUWDdUhhFv7j0yeBIWSCu7RdJoVrmcUUzUnIFaxo/I02SC', 'manager', NULL),
('Alice Employee', 'alice@example.com', '1234567', '$2b$12$AYyBfwkTHP7bj/Z2Dj1pD.CmwWaeNM9QKS/1inlNjuio.NiR0iTHq', 'employee', 1),
('Bob Employee', 'bob@example.com', '7654321', '$2b$12$LusZBu5w0.GqICAwyri./OFaw.s6XQDveaUwdVPACeB7AcwTxqn6W', 'employee', 1),
('Charlie Employee', 'charlie@example.com', '1111111', '$2b$12$RjC299uXPr/GMbg4O1vPoeTKCNTSVuz4FtTqEZIm2WfKwfcpnSkI2', 'employee', 1),
('David Employee', 'david@example.com', '2222222', '$2b$12$iZOYfLXzEByB5l/yw0MmjO28fTX6q0KexaWwCgoVC25Ld56qehd/.', 'employee', 1),
('Eve Employee', 'eve@example.com', '3333333', '$2b$12$eT6.WU14phmhMbspFtou0upBOqsgKYR.qSKAJknTkCdcGK2WstRba', 'employee', 1),
('Frank Employee', 'frank@example.com', '4444444', '$2b$12$gI2o.poJ/0OAm/sAaOH6suEdn6ohsyJyGOJ/gtiCQJWGHGqAhsiE.', 'employee', 1),
('Grace Employee', 'grace@example.com', '5555555', '$2b$12$u2qE9qsUMUZ2nWsBiNblNu6O6rad7Pba/fLUEkkbjgw4K8.cOdYHe', 'employee', 1),
('Hank Employee', 'hank@example.com', '6666666', '$2b$12$Ju8QZ4X9HX/QOK4fec4WWOHJRvmkiDCxx0RhAc6dj7GLs6cKFDsFq', 'employee', 1),
('Ivy Employee', 'ivy@example.com', '7777777', '$2b$12$CO4floxP.TAiiuzKxj3JgOJEfei3sipNMIl92o7jhowts07RxBbCG', 'employee', 1),
('Jack Employee', 'jack@example.com', '8888888', '$2b$12$TNN7xlCrBQ0q7KoDT0ZwBeTPmvg9eTU7dSryNXn851WvwBjCyIedq', 'employee', 1),
('Kate Employee', 'kate@example.com', '9999999', '$2b$12$VFcXHigM/0nWNTfWVlrs1unxdHdwuiDgyyD0AM6jMn7/ID59HROdW', 'employee', 1);

-- Insert sample vacation requests
INSERT INTO vacation_requests (employee_id, start_date, end_date, reason, status, reviewed_by) VALUES
(2, '2024-07-01', '2024-07-10', 'Family trip', 'pending', NULL),
(3, '2024-08-15', '2024-08-20', 'Medical leave', 'approved', 1),
(2, '2024-09-10', '2024-09-15', 'Personal time', 'rejected', 1),
(4, '2024-07-20', '2024-07-25', 'Conference', 'pending', NULL),
(5, '2024-08-05', '2024-08-10', 'Vacation', 'approved', 1),
(6, '2024-09-01', '2024-09-07', 'Personal', 'rejected', 1),
(7, '2024-10-12', '2024-10-18', 'Holiday', 'pending', NULL),
(8, '2024-11-01', '2024-11-05', 'Sick leave', 'approved', 1),
(9, '2024-12-10', '2024-12-15', 'Training', 'rejected', 1);

-- Insert sample audit logs
INSERT INTO audit_logs (user_id, action, details) VALUES
(1, 'Created User', 'Alice Employee was added to the system.'),
(1, 'Created User', 'Bob Employee was added to the system.'),
(1, 'Approved Vacation', 'Approved vacation request for Bob Employee.'),
(1, 'Created User', 'Charlie Employee was added to the system.'),
(1, 'Created User', 'David Employee was added to the system.'),
(1, 'Created User', 'Eve Employee was added to the system.'),
(1, 'Created User', 'Frank Employee was added to the system.'),
(1, 'Created User', 'Grace Employee was added to the system.'),
(1, 'Created User', 'Hank Employee was added to the system.'),
(1, 'Created User', 'Ivy Employee was added to the system.'),
(1, 'Created User', 'Jack Employee was added to the system.'),
(1, 'Created User', 'Kate Employee was added to the system.'),
(1, 'Rejected Vacation', 'Rejected vacation request for David Employee.'),
(1, 'Approved Vacation', 'Approved vacation request for Eve Employee.');

from database.connection import connect_db


class VacationRequestService:
    """Handles vacation request operations."""

    @staticmethod
    def get_vacation_requests(user):
        """Retrieve vacation requests for all employees (Managers only)."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Fetch all vacation requests, including employee details and who reviewed them
            cursor.execute("""
                SELECT vr.id, u.name, u.employee_code, vr.start_date, vr.end_date, vr.reason, vr.status, 
                    r.name AS reviewed_by
                FROM vacation_requests vr
                LEFT JOIN users u ON vr.employee_id = u.id
                LEFT JOIN users r ON vr.reviewed_by = r.id;
            """)

            # Convert query results into a list of dictionaries
            requests = [
                {"id": row[0], "employee_name": row[1], "employee_code": row[2], "start_date": str(row[3]),
                "end_date": str(row[4]), "reason": row[5], "status": row[6], "reviewed_by": row[7] if row[7] else 'Not Reviewed'}
                for row in cursor.fetchall()
            ]
            return requests, 200

        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_vacation_requests_me(user):
        """Retrieve vacation requests for the logged-in employee."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Fetch vacation requests for the logged-in employee
            cursor.execute("""
                SELECT vr.id, vr.start_date, vr.end_date, vr.reason, vr.status, 
                    r.name AS reviewed_by
                FROM vacation_requests vr
                LEFT JOIN users r ON vr.reviewed_by = r.id
                WHERE vr.employee_id = %s;
            """, (user["user_id"],))

            # Convert query results into a list of dictionaries
            requests = [
                {"id": row[0], "start_date": str(row[1]), "end_date": str(row[2]), "reason": row[3],
                "status": row[4], "reviewed_by": row[5] if row[5] else 'Not Reviewed'}
                for row in cursor.fetchall()
            ]
            return requests, 200

        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def create_vacation_request(employee_id, start_date, end_date, reason):
        """Create a new vacation request."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Insert a new vacation request with 'pending' status
            cursor.execute(
                "INSERT INTO vacation_requests (employee_id, start_date, end_date, reason, status, reviewed_by) "
                "VALUES (%s, %s, %s, %s, 'pending', NULL) RETURNING id;",
                (employee_id, start_date, end_date, reason)
            )
            vacation_request_id = cursor.fetchone()[0]
            conn.commit()
            return {"message": "Vacation request created successfully", "id": vacation_request_id}, 201

        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400

    @staticmethod
    def review_vacation_request(request_id, reviewer_id, status):
        """Approve or reject a vacation request and record the reviewer."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Check if the vacation request exists
            cursor.execute("SELECT id, status FROM vacation_requests WHERE id = %s", (request_id,))
            request = cursor.fetchone()

            if not request:
                return {"error": "Vacation request not found"}, 404

            # Update the status and mark the reviewer
            cursor.execute(
                "UPDATE vacation_requests SET status = %s, reviewed_by = %s WHERE id = %s RETURNING id, status, reviewed_by;",
                (status, reviewer_id, request_id)
            )
            updated_request = cursor.fetchone()
            conn.commit()

            return {
                "message": "Vacation request updated successfully",
                "id": updated_request[0],
                "status": updated_request[1],
                "reviewed_by": updated_request[2]
            }, 200

        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400

    @staticmethod
    def delete_vacation_request(request_id, employee_id):
        """Delete a vacation request if it is pending and belongs to the employee."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Retrieve the vacation request details
            cursor.execute("SELECT id, employee_id, status FROM vacation_requests WHERE id = %s", (request_id,))
            request = cursor.fetchone()

            if not request:
                return {"error": "Vacation request not found"}, 404

            # Ensure the employee owns the request and that it is still pending
            if request[1] != employee_id:
                return {"error": "You can only delete your own vacation request"}, 403
            if request[2] != "pending":
                return {"error": "Only pending requests can be deleted"}, 400

            # Delete the vacation request
            cursor.execute("DELETE FROM vacation_requests WHERE id = %s", (request_id,))
            conn.commit()

            return {"message": "Vacation request deleted successfully"}, 200

        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400

    @staticmethod
    def get_vacation_request_by_id(request_id):
        """Retrieve details of a single vacation request."""
        conn = connect_db()
        cursor = conn.cursor()
        
        # Fetch the vacation request details
        cursor.execute("SELECT id, employee_id, start_date, end_date, status FROM vacation_requests WHERE id = %s", (request_id,))
        request = cursor.fetchone()

        if not request:
            return {"error": "Vacation request not found"}, 404

        return {
            "id": request[0],
            "employee_id": request[1],
            "start_date": request[2],
            "end_date": request[3],
            "status": request[4]
        }, 200

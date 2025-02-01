from database.connection import connect_db
from api.auth import AuthService

class VacationRequestService:
    """ Handles vacation request-related operations (business logic). """

from database.connection import connect_db

class VacationRequestService:
    """Handles vacation request operations."""

    @staticmethod
    def get_vacation_requests(user):
        """Retrieve vacation requests. Managers see all, employees see their own."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            if user["role"] == "manager":
                cursor.execute("SELECT id, employee_id, start_date, end_date, status FROM vacation_requests;")
            else:
                cursor.execute(
                    "SELECT id, employee_id, start_date, end_date, status FROM vacation_requests WHERE employee_id = %s;",
                    (user["user_id"],)
                )

            requests = [
                {"id": row[0], "employee_id": row[1], "start_date": str(row[2]), "end_date": str(row[3]), "status": row[4]}
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
            # Insert the new vacation request with status 'pending' and reviewed_by 'NULL'
            cursor.execute(
                "INSERT INTO vacation_requests (employee_id, start_date, end_date, reason, status, reviewed_by) "
                "VALUES (%s, %s, %s, %s, 'pending', NULL) RETURNING id;",
                (employee_id, start_date, end_date, reason)
            )
            # Commit the transaction and fetch the new request ID
            vacation_request_id = cursor.fetchone()[0]
            conn.commit()
            
            # Return success response
            return {"message": "Vacation request created successfully", "id": vacation_request_id}, 201

        except Exception as e:
            conn.rollback()  # Ensure the transaction is rolled back on error
            return {"error": str(e)}, 400

    @staticmethod
    def review_vacation_request(request_id, reviewer_id, status):
        """Approve or reject a vacation request and set who reviewed it."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Check if the vacation request exists
            cursor.execute("SELECT id, status FROM vacation_requests WHERE id = %s", (request_id,))
            request = cursor.fetchone()

            if not request:
                return {"error": "Vacation request not found"}, 404
            
            # Update the status and reviewed_by fields
            cursor.execute(
                "UPDATE vacation_requests SET status = %s, reviewed_by = %s WHERE id = %s RETURNING id, status, reviewed_by;",
                (status, reviewer_id, request_id)
            )
            updated_request = cursor.fetchone()
            conn.commit()

            # Return success response with updated information
            return {
                "message": "Vacation request updated successfully",
                "id": updated_request[0],
                "status": updated_request[1],
                "reviewed_by": updated_request[2]
            }, 200

        except Exception as e:
            conn.rollback()  # Ensure the transaction is rolled back on error
            return {"error": str(e)}, 400
        
    @staticmethod
    def get_vacation_request_by_id(request_id):
        """ Retrieves details of a single vacation request. """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, start_date, end_date, status FROM vacation_requests WHERE id = %s", (request_id,))
        request = cursor.fetchone()

        if not request:
            return {"error": "Vacation request not found"}, 404

        return {"id": request[0], "user_id": request[1], "start_date": request[2], "end_date": request[3], "status": request[4]}, 200
    """
    @staticmethod
        def update_vacation_request(request_id, data):
         Updates a vacation request's details (Manager only, allows partial updates). 
        conn = connect_db()
        cursor = conn.cursor()

        # Prepare update query dynamically based on provided fields
        update_fields = []
        update_values = []

        if "start_date" in data:
            update_fields.append("start_date = %s")
            update_values.append(data["start_date"])
    """


            
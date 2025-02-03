from database.connection import connect_db
from api.auth import AuthService


class UserService:
    """Handles user-related operations (business logic)."""

    @staticmethod
    def create_user(data, created_by):
        """Creates a new user (Manager only)."""
        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, employee_code, password_hash, role, created_by) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                (data["name"], data["email"], data["employee_code"], AuthService.hash_password(data["password"]), data["role"], created_by)
            )
            conn.commit()
            user_id = cursor.fetchone()[0]
            return {"message": "User created", "user_id": user_id}, 201
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400

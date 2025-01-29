from database.connection import connect_db
from api.auth import AuthService

class UserService:
    """ Handles user-related operations (business logic). """

    @staticmethod
    def create_user(data, created_by):
        """ Creates a new user (Manager only). """
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

    @staticmethod
    def get_users():
        """ Retrieves all users (Manager only). """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, role FROM users")
        users = [{"id": row[0], "name": row[1], "email": row[2], "role": row[3]} for row in cursor.fetchall()]
        return users, 200

    @staticmethod
    def update_user(user_id, data):
        """ Updates a user's details (Manager only, allows partial updates). """
        conn = connect_db()
        cursor = conn.cursor()

        # Prepare update query dynamically based on provided fields
        update_fields = []
        update_values = []

        if "name" in data:
            update_fields.append("name = %s")
            update_values.append(data["name"])

        if "email" in data:
            update_fields.append("email = %s")
            update_values.append(data["email"])

        if "password" in data:
            update_fields.append("password_hash = %s")
            update_values.append(AuthService.hash_password(data["password"]))

        # If no fields were provided, return an error
        if not update_fields:
            return {"error": "No fields provided for update"}, 400

        # Add user_id as the last value for the WHERE clause
        update_values.append(user_id)

        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING id;"
        
        try:
            cursor.execute(query, tuple(update_values))
            if cursor.rowcount == 0:
                return {"error": "User not found"}, 404
            conn.commit()
            return {"message": "User updated successfully"}, 200
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400


    @staticmethod
    def delete_user(user_id, requesting_user_id):
        """ Deletes a user (Manager only, but cannot delete themselves). """
        if user_id == requesting_user_id:
            return {"error": "Managers cannot delete themselves"}, 403

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
            if cursor.rowcount == 0:
                return {"error": "User not found"}, 404
            conn.commit()
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 400

"""
    @staticmethod
    def get_me(user_id):
        Retrieves the currently authenticated user's details. 
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return {"error": "User not found"}, 404
        return {"id": user[0], "name": user[1], "email": user[2], "role": user[3]}, 200
"""


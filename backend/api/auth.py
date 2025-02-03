import os
import jwt
import bcrypt
import datetime
from database.connection import connect_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


class AuthService:
    """Handles user authentication (login, password hashing, JWT)."""

    @staticmethod
    def hash_password(password):
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        """Verifies a password against a stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def generate_jwt(user_id, role):
        """Generates a JWT token for authentication."""
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expires in 2 hours
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def login(email, password):
        """Authenticates a user and returns a JWT token if successful."""
        conn = connect_db()
        cursor = conn.cursor()

        # Find user by email
        cursor.execute("SELECT id, password_hash, role FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not AuthService.verify_password(password, user[1]):
            return {"error": "Invalid email or password"}, 401

        # Generate JWT
        token = AuthService.generate_jwt(user[0], user[2])

        return {"message": "Login successful", "token": token, "role": user[2]}, 200  # Return token and role

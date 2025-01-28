import os
import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

class AuthMiddleware:
    """ Middleware to validate JWT tokens. """

    @staticmethod
    def validate_token(token):
        """ Validates a JWT token and returns user details or None if invalid. """
        if not token or not token.startswith("Bearer "):
            return None

        try:
            decoded = jwt.decode(token.split("Bearer ")[1], SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

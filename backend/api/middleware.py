import os
import jwt
from functools import wraps
from dotenv import load_dotenv
from werkzeug.wrappers import Response
import json

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

class AuthMiddleware:
    """ Middleware to validate JWT tokens globally. """

    @staticmethod
    def require_auth(required_role):
        """ Decorator to require authentication for a route. """
        def decorator(func):
            @wraps(func)
            def wrapper(instance, request, *args, **kwargs):
                token = request.headers.get("Authorization")
                if not token or not token.startswith("Bearer "):
                    return Response(json.dumps({"error": "Unauthorized"}), status=401, mimetype="application/json")

                try:
                    decoded = jwt.decode(token.split("Bearer ")[1], SECRET_KEY, algorithms=["HS256"])
                    if decoded["role"] != required_role:
                        return Response(json.dumps({"error": "Forbidden"}), status=403, mimetype="application/json")
                    return func(instance, request, decoded, *args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return Response(json.dumps({"error": "Token expired"}), status=401, mimetype="application/json")
                except jwt.InvalidTokenError:
                    return Response(json.dumps({"error": "Invalid token"}), status=401, mimetype="application/json")

            return wrapper
        return decorator

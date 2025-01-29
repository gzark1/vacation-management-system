from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from api.routes import url_map
from api.middleware import AuthMiddleware
import json

class App:
    """Main Application Class for handling routing and requests."""

    def __call__(self, environ, start_response):
        request = Request(environ)
        urls = url_map.bind_to_environ(environ)

        try:
            endpoint, args = urls.match()
            handler = getattr(self, endpoint)
            response = handler(request, **args)
        except Exception as e:
            response = Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")

        return response(environ, start_response)

    def login(self, request):
        """Handle user login."""
        data = request.get_json()
        from api.auth import AuthService
        response, status_code = AuthService.login(data.get("email"), data.get("password"))
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("manager")
    def create_user(self, request, user):
        """Create a new user (Manager only)."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.create_user(data, user["user_id"])
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("manager")
    def get_users(self, request, user):
        """Get all users (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.get_users()
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("manager")
    def update_user(self, request, user, user_id):
        """Update a user (Manager only)."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.update_user(user_id, data)
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("manager")
    def delete_user(self, request, user, user_id):
        """Delete a user (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.delete_user(user_id, user["user_id"])
        return Response(json.dumps(response), status=status_code, mimetype="application/json")
    
"""
    @AuthMiddleware.require_auth()
    def get_me(self, request, user):
        Get currently authenticated user.
        from api.users import UserService
        response, status_code = UserService.get_me(user["user_id"])
        return Response(json.dumps(response), status=status_code, mimetype="application/json")
"""
    

if __name__ == "__main__":
    app = App()
    print("Server running on port 8080...")
    run_simple("0.0.0.0", 8080, app)

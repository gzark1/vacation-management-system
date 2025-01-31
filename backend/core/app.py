from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from api.routes import url_map
from api.middleware import AuthMiddleware
import traceback
import json
from api.vacation_requests import VacationRequestService

class App:
    """Main Application Class for handling routing and requests."""
    def __call__(self, environ, start_response):
        request = Request(environ)
        urls = url_map.bind_to_environ(environ)
        if request.method == "OPTIONS":
            return self.options(request)(environ, start_response)

        try:
            endpoint, args = urls.match()
            handler = getattr(self, endpoint)
            response = handler(request, **args)
        except Exception as e:
            # Capture and print full error traceback
            error_message = traceback.format_exc()
            print(f"🔥 Backend Error:\n{error_message}")  # Logs full stack trace

            response = Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")

        # Add CORS headers to every response
        response.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response(environ, start_response)

    def login(self, request):
        """Handle user login."""
        data = request.get_json()
        from api.auth import AuthService
        response, status_code = AuthService.login(data.get("email"), data.get("password"))
        return self.create_response(response, status_code)

    def logout(self, request):
        """Handles user logout."""
        return self.create_response({"message": "Logged out successfully"}, 200)

    @AuthMiddleware.require_auth("manager")
    def create_user(self, request, user):
        """Create a new user (Manager only)."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.create_user(data, user["user_id"])
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def get_users(self, request, user):
        """Get all users (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.get_users()
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def update_user(self, request, user, user_id):
        """Update a user (Manager only)."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.update_user(user_id, data)
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def delete_user(self, request, user, user_id):
        """Delete a user (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.delete_user(user_id, user["user_id"])
        return self.create_response(response, status_code)
    
    @AuthMiddleware.require_auth("manager")
    def get_user_by_id(self, request, user, user_id):
        """Retrieve a single user's details (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.get_user_by_id(user_id)
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth()
    def get_vacation_requests(self, request, user):
        """Retrieve vacation requests. Managers see all, employees see their own."""
        response, status_code = VacationRequestService.get_vacation_requests(user)
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    def options(self, request):
        """Handles CORS preflight requests for all endpoints."""
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.status_code = 200  # Explicitly return HTTP 200 for preflight
        return response

    def create_response(self, data, status_code):
        return Response(
            json.dumps(data),
            status=status_code,
            mimetype="application/json"
        )

if __name__ == "__main__":
    app = App()
    print("Server running on port 8080...")
    run_simple("0.0.0.0", 8080, app)
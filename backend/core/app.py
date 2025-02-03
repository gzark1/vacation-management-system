from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from api.routes import url_map
from api.middleware import AuthMiddleware
import traceback
import json
from api.vacation_requests import VacationRequestService

class App:
    """Main application class for handling routing and requests."""

    def __call__(self, environ, start_response):
        """Handles incoming HTTP requests and dispatches them to the correct handler."""
        request = Request(environ)
        urls = url_map.bind_to_environ(environ)

        # Handle CORS preflight requests
        if request.method == "OPTIONS":
            return self.options(request)(environ, start_response)

        try:
            # Match the requested URL to a defined route
            endpoint, args = urls.match()
            handler = getattr(self, endpoint)
            response = handler(request, **args)
        except Exception as e:
            # Capture and log full error traceback for debugging
            error_message = traceback.format_exc()
            print(f"🔥 Backend Error:\n{error_message}")

            response = Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")

        # Set CORS headers for cross-origin requests
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response(environ, start_response)

    def login(self, request):
        """Handles user login and returns a JWT token if successful."""
        data = request.get_json()
        from api.auth import AuthService
        response, status_code = AuthService.login(data.get("email"), data.get("password"))
        return self.create_response(response, status_code)

    def logout(self, request):
        """Handles user logout (currently a placeholder)."""
        return self.create_response({"message": "Logged out successfully"}, 200)

    @AuthMiddleware.require_auth("manager")
    def create_user(self, request, user):
        """Allows managers to create new users."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.create_user(data, user["user_id"])
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def get_users(self, request, user):
        """Retrieves all users (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.get_users()
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def update_user(self, request, user, user_id):
        """Allows managers to update user details."""
        data = request.get_json()
        from api.users import UserService
        response, status_code = UserService.update_user(user_id, data)
        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def delete_user(self, request, user, user_id):
        """Allows managers to delete a user."""
        from api.users import UserService
        response, status_code = UserService.delete_user(user_id, user["user_id"])
        return self.create_response(response, status_code)
    
    @AuthMiddleware.require_auth("manager")
    def get_user_by_id(self, request, user, user_id):
        """Retrieves a single user's details (Manager only)."""
        from api.users import UserService
        response, status_code = UserService.get_user_by_id(user_id)
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("employee")
    def create_vacation_request(self, request, user):
        """Allows employees to submit a vacation request."""
        data = request.get_json()

        # Validate required fields
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        reason = data.get("reason")

        if not start_date or not end_date or not reason:
            return self.create_response({"error": "start_date, end_date, and reason are required."}, 400)

        from api.vacation_requests import VacationRequestService
        response, status_code = VacationRequestService.create_vacation_request(user["user_id"], start_date, end_date, reason)

        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def review_vacation_request(self, request, user, request_id):
        """Allows managers to approve or reject a vacation request."""
        data = request.get_json()
        status = data.get("status")

        if status not in ["approved", "rejected"]:
            return self.create_response({"error": "Invalid status. Must be 'approved' or 'rejected'."}, 400)

        from api.vacation_requests import VacationRequestService
        response, status_code = VacationRequestService.review_vacation_request(request_id, user["user_id"], status)

        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("employee")
    def delete_vacation_request(self, request, user, request_id):
        """Allows employees to delete a pending vacation request."""
        from api.vacation_requests import VacationRequestService
        response, status_code = VacationRequestService.delete_vacation_request(request_id, user["user_id"])

        return self.create_response(response, status_code)

    @AuthMiddleware.require_auth("manager")
    def get_vacation_requests(self, request, user):
        """Retrieves all vacation requests (Manager only)."""
        from api.vacation_requests import VacationRequestService
        response, status_code = VacationRequestService.get_vacation_requests(user)
        return Response(json.dumps(response), status=status_code, mimetype="application/json")

    @AuthMiddleware.require_auth("employee")
    def get_vacation_requests_me(self, request, user):
        """Retrieves the vacation requests for the logged-in employee."""
        from api.vacation_requests import VacationRequestService
        response, status_code = VacationRequestService.get_vacation_requests_me(user)
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
        """Helper method to create a JSON response."""
        return Response(
            json.dumps(data),
            status=status_code,
            mimetype="application/json"
        )


if __name__ == "__main__":
    # Start the application server
    app = App()
    print("Server running on port 8080...")
    run_simple("0.0.0.0", 8080, app)

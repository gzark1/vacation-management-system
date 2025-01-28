import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from api.auth import AuthService
from api.middleware import AuthMiddleware

class RequestHandler(BaseHTTPRequestHandler):
    """ Handles API requests (authentication routes only for now). """

    def do_POST(self):
        """ Handle POST requests (login). """
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        if self.path == "/login":
            self.handle_login(data)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_login(self, data):
        """ Handles user login and returns a JWT token. """
        response, status_code = AuthService.login(data.get("email"), data.get("password"))
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        """ Handle GET requests (protected test route). """
        if self.path == "/protected":
            self.handle_protected()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_protected(self):
        """ Example of a protected route requiring a valid JWT token. """
        token = self.headers.get("Authorization")
        user = AuthMiddleware.validate_token(token)

        if not user:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid or expired token"}).encode())
            return

        response = {"message": f"Hello, {user['role']}! You have access to this route."}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

# Run the server
if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 8080...")
    httpd.serve_forever()

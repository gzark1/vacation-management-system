from werkzeug.routing import Map, Rule

url_map = Map([
    # Authentication Routes
    Rule('/login', methods=['POST'], endpoint='login'),
    Rule('/logout', methods=['POST'], endpoint='logout'),

    # User Management
    Rule('/users', methods=['GET'], endpoint='get_users'),
    Rule('/users', methods=['POST'], endpoint='create_user'),
    Rule('/users/<int:user_id>', methods=['PUT'], endpoint='update_user'),  
    Rule('/users/<int:user_id>', methods=['DELETE'], endpoint='delete_user'),
    Rule('/users/<int:user_id>', methods=['GET'], endpoint='get_user_by_id'),

    # Vacation Requests
    Rule('/vacation_requests', methods=['GET'], endpoint='get_vacation_requests'),
    Rule('/vacation_requests/me', methods=['GET'], endpoint='get_vacation_requests_me'),
    Rule('/vacation_requests', methods=['POST'], endpoint='create_vacation_request'),
    Rule('/vacation_requests/<int:request_id>/review', methods=['POST'], endpoint='review_vacation_request'),
    Rule('/vacation_requests/<int:request_id>', methods=['DELETE'], endpoint='delete_vacation_request'),
    #Rule('/me', methods=['GET'], endpoint='get_me'),  # ✅ Get logged-in user,, under development. 
])



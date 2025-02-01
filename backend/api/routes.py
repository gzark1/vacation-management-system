from werkzeug.routing import Map, Rule

url_map = Map([
    ## Auth
    Rule('/login', methods=['POST'], endpoint='login'),
    Rule('/logout', methods=['POST'], endpoint='logout'),
    ## Users
    Rule('/users', methods=['GET'], endpoint='get_users'),
    Rule('/users', methods=['POST'], endpoint='create_user'),
    Rule('/users/<int:user_id>', methods=['PUT'], endpoint='update_user'),  # ✅ Update user
    Rule('/users/<int:user_id>', methods=['DELETE'], endpoint='delete_user'),  # ✅ Delete user
    Rule('/users/<int:user_id>', methods=['GET'], endpoint='get_user_by_id'),  # ✅ Get user
    ## Vacation requests
    Rule('/vacation_requests', methods=['GET'], endpoint='get_vacation_requests'), # ✅ Get requests, manager sees all, employee sees their own
    Rule('/vacation_requests', methods=['POST'], endpoint='create_vacation_request'),
    Rule('/vacation_requests/<int:request_id>/review', methods=['POST'], endpoint='review_vacation_request'),
    Rule('/vacation_requests/<int:request_id>', methods=['DELETE'], endpoint='delete_vacation_request'),  # ✅ Delete request
    #Rule('/me', methods=['GET'], endpoint='get_me'),  # ✅ Get logged-in user
])



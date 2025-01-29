from werkzeug.routing import Map, Rule

url_map = Map([
    Rule('/login', methods=['POST'], endpoint='login'),
    Rule('/logout', methods=['POST'], endpoint='logout'),
    Rule('/users', methods=['POST'], endpoint='create_user'),
    Rule('/users', methods=['GET'], endpoint='get_users'),
    Rule('/users/<int:user_id>', methods=['PUT'], endpoint='update_user'),  # ✅ Update user
    Rule('/users/<int:user_id>', methods=['DELETE'], endpoint='delete_user'),  # ✅ Delete user
    #Rule('/me', methods=['GET'], endpoint='get_me'),  # ✅ Get logged-in user
])

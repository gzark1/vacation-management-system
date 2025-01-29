from werkzeug.routing import Map, Rule

url_map = Map([
    Rule('/login', methods=['POST'], endpoint='login'),
    Rule('/users', methods=['POST'], endpoint='create_user'),
    Rule('/users', methods=['GET'], endpoint='get_users'),
])

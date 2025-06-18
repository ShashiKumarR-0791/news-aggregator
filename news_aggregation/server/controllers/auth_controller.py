from server.services.auth_service import AuthService

auth_service = AuthService()

def signup_handler(data, _):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")
    return auth_service.register_user(username, email, password, role)

def login_handler(data, _):
    email = data.get("email")
    password = data.get("password")
    return auth_service.login_user(email, password)

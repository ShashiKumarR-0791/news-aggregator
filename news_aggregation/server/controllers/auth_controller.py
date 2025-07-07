from server.services.auth_service import AuthService
import re

auth_service = AuthService()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    return len(password) >= 6

def signup_handler(data, _):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    role = "user"

    if not username or not email or not password:
        return {"status": "error", "message": "All fields are required."}

    if not is_valid_email(email):
        return {"status": "error", "message": "Invalid email format."}

    if not is_strong_password(password):
        return {"status": "error", "message": "Password must be at least 6 characters long."}

    return auth_service.register_user(username, email, password, role)

def login_handler(data, _):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"status": "error", "message": "Email and password are required."}

    return auth_service.login_user(email, password)

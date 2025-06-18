import hashlib
from server.models.user import User
from server.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password, role='user'):
        if self.user_repo.find_by_username_or_email(username) or self.user_repo.find_by_username_or_email(email):
            return {"success": False, "message": "User already exists"}
        password_hash = self.hash_password(password)
        user = User(username=username, email=email, password_hash=password_hash, role=role)
        self.user_repo.create_user(user)
        return {"success": True, "message": "User registered successfully"}

    def login_user(self, email, password):
        password_hash = self.hash_password(password)
        user = self.user_repo.find_by_credentials(email, password_hash)
        if user:
            return {"success": True, "user": user}
        return {"success": False, "message": "Invalid credentials"}

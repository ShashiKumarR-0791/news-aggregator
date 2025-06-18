from server.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, username, email, password_hash, role='user', is_active=True):
        super().__init__()
        self.user_id = None
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at,
            "is_active": self.is_active
        }

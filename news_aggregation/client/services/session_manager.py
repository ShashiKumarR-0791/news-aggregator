class SessionManager:
    def __init__(self):
        self.user = None
        self.token = None

    def login(self, user, token):
        self.user = user
        self.token = token

    def logout(self):
        self.user = None
        self.token = None

    def get_user(self):
        return self.user

    def get_role(self):
        return self.user.get("role") if self.user else None

    def get_token(self):
        return self.token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        } if self.token else {
            "Content-Type": "application/json"
        }

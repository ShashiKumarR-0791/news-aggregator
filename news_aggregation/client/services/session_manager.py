class SessionManager:
    def __init__(self):
        self.user = None

    def login(self, user_data):
        self.user = user_data

    def logout(self):
        self.user = None

    def is_logged_in(self):
        return self.user is not None

    def get_role(self):
        return self.user.get("role") if self.user else None

    def get_user_id(self):
        return self.user.get("user_id") if self.user else None

class Session:
    def __init__(self):
        self.user = None
        self.token = None

    def login(self, user, token):
        self.user = user
        self.token = token

    def logout(self):
        self.user = None
        self.token = None

    def is_authenticated(self):
        return self.user is not None and self.token is not None

    def get_user(self):
        return self.user

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        } if self.token else {
            "Content-Type": "application/json"
        }



session = Session()

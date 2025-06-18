from server.models.base_model import BaseModel

class NotificationConfig(BaseModel):
    def __init__(self, user_id, category, is_enabled=True, keywords=''):
        super().__init__()
        self.config_id = None
        self.user_id = user_id
        self.category = category
        self.is_enabled = is_enabled
        self.keywords = keywords

    def to_dict(self):
        return {
            "config_id": self.config_id,
            "user_id": self.user_id,
            "category": self.category,
            "is_enabled": self.is_enabled,
            "keywords": self.keywords,
            "created_at": self.created_at
        }

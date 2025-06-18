from server.models.base_model import BaseModel

class Notification(BaseModel):
    def __init__(self, user_id, message, type='info', is_read=False):
        super().__init__()
        self.notification_id = None
        self.user_id = user_id
        self.message = message
        self.type = type
        self.is_read = is_read

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "type": self.type,
            "is_read": self.is_read,
            "created_at": self.created_at
        }

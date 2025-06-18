from server.models.base_model import BaseModel

class ExternalServer(BaseModel):
    def __init__(self, name, api_url, api_key, is_active=True):
        super().__init__()
        self.server_id = None
        self.name = name
        self.api_url = api_url
        self.api_key = api_key
        self.is_active = is_active
        self.last_accessed = None

    def to_dict(self):
        return {
            "server_id": self.server_id,
            "name": self.name,
            "api_url": self.api_url,
            "api_key": self.api_key,
            "is_active": self.is_active,
            "last_accessed": self.last_accessed,
            "created_at": self.created_at
        }

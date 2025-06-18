from server.models.base_model import BaseModel

class Category(BaseModel):
    def __init__(self, name, description='', is_active=True):
        super().__init__()
        self.category_id = None
        self.name = name
        self.description = description
        self.is_active = is_active

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "is_active": self.is_active
        }

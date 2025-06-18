from server.models.base_model import BaseModel

class SavedArticle(BaseModel):
    def __init__(self, user_id, article_id):
        super().__init__()
        self.saved_id = None
        self.user_id = user_id
        self.article_id = article_id

    def to_dict(self):
        return {
            "saved_id": self.saved_id,
            "user_id": self.user_id,
            "article_id": self.article_id,
            "saved_at": self.created_at
        }

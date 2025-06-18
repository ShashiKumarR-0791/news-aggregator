from server.models.base_model import BaseModel

class NewsArticle(BaseModel):
    def __init__(self, title, description, content, url, source, category_id=None, published_at=None, likes=0, dislikes=0):
        super().__init__()
        self.article_id = None
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.source = source
        self.category_id = category_id
        self.published_at = published_at
        self.likes = likes
        self.dislikes = dislikes

    def to_dict(self):
        return {
            "article_id": self.article_id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "category_id": self.category_id,
            "published_at": self.published_at,
            "created_at": self.created_at,
            "likes": self.likes,
            "dislikes": self.dislikes
        }

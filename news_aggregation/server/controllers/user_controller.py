from server.repositories.news_repository import NewsRepository
from server.repositories.user_repository import UserRepository
from server.repositories.notification_repository import NotificationRepository
from server.models.saved_article import SavedArticle
from server.repositories.base_repository import BaseRepository

class UserController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.news_repo = NewsRepository()
        self.notif_repo = NotificationRepository()
        self.base_repo = BaseRepository()
    

    def save_article(self, request, user):
        try:
            if hasattr(request, "json"):
                data = request.json()
            else:
                data = request  
            user_id = user.get("user_id") if user else None
            if not user_id:
                email = data.get("email")
                if not email:
                    return {"error": "Missing email or user_id", "status": 400}
                user_obj = self.user_repo.get_user_by_email(email)
                if not user_obj:
                    return {"error": "User not found for provided email", "status": 404}
                user_id = user_obj.get("user_id")
            article_id = data.get("article_id")

            if not user_id or not article_id:
                return {"error": "Missing user_id or article_id", "status": 400}

            query = '''
                INSERT OR IGNORE INTO saved_articles (user_id, article_id, saved_at)
                VALUES (?, ?, datetime('now'))
            '''
            self.base_repo.execute(query, (user_id, article_id))
            return {"message": "Article saved successfully.", "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}



    def delete_saved_article(self, data, user):
        user_id = user.get("user_id")
        article_id = data.get("article_id")
        query = 'DELETE FROM saved_articles WHERE user_id = ? AND article_id = ?'
        self.base_repo.execute(query, (user_id, article_id))
        return {"message": "Article removed from saved list.", "status": 200}

    def get_saved_articles(self, request, user):
        user_id = user.get("user_id")
        query = '''
            SELECT na.* FROM saved_articles sa
            JOIN news_articles na ON na.article_id = sa.article_id
            WHERE sa.user_id = ?
        '''
        rows = self.base_repo.fetchall(query, (user_id,))
        return {"articles": [dict(r) for r in rows], "status": 200}


    @staticmethod
    def delete_user(request, user):
        if user.get("role") != "admin":
            return {"error": "Unauthorized", "status": 403}

        user_id = request.get("user_id_to_delete")
        if not user_id:
            return {"error": "User ID required", "status": 400}

        success = UserRepository().delete_user_by_id(user_id)
        if success:
            return {"message": "User deleted", "status": 200}
        return {"error": "Failed to delete user", "status": 500}

    @staticmethod
    def promote_user(request, user):
        if user.get("role") != "admin":
            return {"error": "Unauthorized", "status": 403}

        user_id = request.get("user_id_to_promote")
        if not user_id:
            return {"error": "User ID required", "status": 400}

        updated = UserRepository().update_user_role(user_id, "admin")
        if updated:
            return {"message": "User promoted to admin", "status": 200}
        return {"error": "Failed to update role", "status": 500}
    
from server.repositories.base_repository import BaseRepository
from server.models.user import User

class UserRepository(BaseRepository):
    def create_user(self, user: User):
        query = '''
            INSERT INTO users (username, email, password_hash, role, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            user.username,
            user.email,
            user.password_hash,
            user.role,
            int(user.is_active),
            user.created_at
        ))

    def find_by_username_or_email(self, username_or_email):
        query = 'SELECT * FROM users WHERE username = ? OR email = ?'
        row = self.fetchone(query, (username_or_email, username_or_email))
        return dict(row) if row else None

    def find_by_credentials(self, email, password_hash):
        query = 'SELECT * FROM users WHERE email = ? AND password_hash = ?'
        row = self.fetchone(query, (email, password_hash))
        return dict(row) if row else None

    def get_all_users(self):
        query = 'SELECT * FROM users'
        rows = self.fetchall(query)
        return [dict(row) for row in rows]

    def delete_user_by_id(self, user_id):
        query = "DELETE FROM users WHERE user_id = ?"
        self.execute(query, (user_id,))
        return True

    def save_article(self, request, user=None):
        try:
            user_id = user.get("user_id") if user else request.get("user_id")
            article_id = request.get("article_id")

            if not user_id or not article_id:
                return {
                    "status": "error",
                    "message": "Missing user_id or article_id"
                }, 400

            self.user_repo.save_article(user_id, article_id)

            return {
                "status": "success",
                "message": "Article saved successfully"
            }, 200

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500


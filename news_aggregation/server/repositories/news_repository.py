from server.repositories.base_repository import BaseRepository
from server.models.news_article import NewsArticle

class NewsRepository(BaseRepository):
    def add_news(self, article: NewsArticle):
        try:
            query = '''
            INSERT OR IGNORE INTO news_articles
            (title, description, content, url, source, category_id, published_at, created_at, likes, dislikes)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)
            '''
            params = (
                article.title, article.description, article.content,
                article.url, article.source, article.category_id,
                article.published_at, article.likes, article.dislikes
            )
            self.execute(query, params)
        except Exception as e:
            print(f" Error saving article: {e}")
    def get_today_articles(self):
        query = """
            SELECT * FROM news_articles
            WHERE date(published_at) = date('now')  -- remove 'localtime'
            ORDER BY published_at DESC
        """
        return self.fetchall(query)


    def get_news_by_date(self, date_str):
        query = "SELECT * FROM news_articles WHERE date(published_at) = ?"
        rows = self.fetchall(query, (date_str,))
        return [dict(row) for row in rows] if rows else []



    def get_news_by_range(self, start, end):
        query = '''
            SELECT * FROM news_articles WHERE DATE(published_at) BETWEEN DATE(?) AND DATE(?)
        '''
        rows = self.fetchall(query, (start, end))
        return [dict(row) for row in rows]
    def get_news_by_date_and_category(self, date, category_id):
        query = """
            SELECT * FROM news_articles
            WHERE DATE(substr(published_at, 1, 10)) = ? AND category_id = ?
            ORDER BY published_at DESC
        """
        return self.fetchall(query, (date, category_id))
    def search_articles(self, keyword, start_date, end_date):
        query = """
            SELECT * FROM news_articles
            WHERE (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)
            AND DATE(published_at) BETWEEN DATE(?) AND DATE(?)
            ORDER BY (likes - dislikes) DESC
        """
        like_term = f"%{keyword.lower()}%"
        rows = self.fetchall(query, (like_term, like_term, start_date, end_date))
        return [dict(row) for row in rows]
    def increment_like(self, article_id):
        query = "UPDATE news_articles SET likes = likes + 1 WHERE article_id = ?"
        self.execute(query, (article_id,))

    def increment_dislike(self, article_id):
        query = "UPDATE news_articles SET dislikes = dislikes + 1 WHERE article_id = ?"
        self.execute(query, (article_id,))



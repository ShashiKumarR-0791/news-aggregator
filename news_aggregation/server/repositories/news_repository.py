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
            print(f"❌ Error saving article: {e}")

    def get_news_by_date(self, date_str):
        query = '''
            SELECT * FROM news_articles WHERE DATE(published_at) = DATE(?)
        '''
        rows = self.fetchall(query, (date_str,))
        return [dict(row) for row in rows]

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


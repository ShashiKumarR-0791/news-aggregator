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
            WHERE date(published_at) = date('now') AND is_hidden = 0
            ORDER BY published_at DESC
        """
        return self.fetchall(query)


    def get_news_by_date(self, date_str):
        query = "SELECT * FROM news_articles WHERE date(published_at) = ? AND is_hidden = 0"
        rows = self.fetchall(query, (date_str,))
        return [dict(row) for row in rows] if rows else []



    def get_news_by_range(self, start, end):
        query = '''
            SELECT * FROM news_articles WHERE DATE(published_at) BETWEEN DATE(?) AND DATE(?) AND is_hidden = 0
        '''
        rows = self.fetchall(query, (start, end))
        return [dict(row) for row in rows]
    def get_news_by_date_and_category(self, date, category_id):
        query = """
            SELECT * FROM news_articles
            WHERE DATE(substr(published_at, 1, 10)) = ? AND category_id = ? AND is_hidden = 0
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
        self.execute("UPDATE news_articles SET likes = likes + 1, dislikes = CASE WHEN dislikes > 0 THEN dislikes - 1 ELSE 0 END WHERE article_id = ?", (article_id,))

    def increment_dislike(self, article_id):
        self.execute("UPDATE news_articles SET dislikes = dislikes + 1, likes = CASE WHEN likes > 0 THEN likes - 1 ELSE 0 END WHERE article_id = ?", (article_id,))
    def search_articles_by_keyword(self, keyword, start_date=None, end_date=None):
        query = '''
            SELECT * FROM news_articles
            WHERE (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)
        '''
        like_term = f"%{keyword.lower()}%"
        params = [like_term, like_term]

        if start_date:
            query += " AND published_at >= ?"
            params.append(start_date)
        if end_date:
            query += " AND published_at <= ?"
            params.append(end_date)

        query += " ORDER BY published_at DESC"
        return [dict(row) for row in self.fetchall(query, tuple(params))]
    def add_report(self, article_id):
        query = '''
            INSERT INTO article_reports (article_id) VALUES (?)
        '''
        self.execute(query, (article_id,))
        count_query = 'SELECT COUNT(*) FROM article_reports WHERE article_id = ?'
        count = self.fetchone(count_query, (article_id,))[0]
        if count >= 3:
            self.execute('UPDATE news_articles SET is_hidden = 1 WHERE article_id = ?', (article_id,))
        return count
    def get_reported_articles(self, threshold=1):
        query = """
            SELECT a.article_id, a.title, a.source, a.published_at, a.is_hidden,
                   COUNT(r.report_id) AS report_count
            FROM news_articles a
            JOIN article_reports r ON a.article_id = r.article_id
            GROUP BY a.article_id
            HAVING report_count >= ?
            ORDER BY report_count DESC, a.created_at DESC
        """
        rows = self.fetchall(query, (threshold,))
        return [dict(row) for row in rows]

    def delete_article(self, article_id):
        """Permanently delete an article and all its related data"""
        try:
            # Delete related records first (due to foreign key constraints)
            self.execute('DELETE FROM article_reports WHERE article_id = ?', (article_id,))
            self.execute('DELETE FROM saved_articles WHERE article_id = ?', (article_id,))
            # Delete the article itself
            self.execute('DELETE FROM news_articles WHERE article_id = ?', (article_id,))
            return True
        except Exception as e:
            print(f"Error deleting article: {e}")
            return False




    def unhide_article(self, article_id):
        query = 'UPDATE news_articles SET is_hidden = 0 WHERE article_id = ?'
        self.execute(query, (article_id,))

    def get_most_liked_articles(self, limit=20):
        query = """
            SELECT * FROM news_articles 
            WHERE likes > 0 AND is_hidden = 0
            ORDER BY likes DESC, published_at DESC
            LIMIT ?
        """
        rows = self.fetchall(query, (limit,))
        return [dict(row) for row in rows]

    def get_hidden_articles(self):
        query = "SELECT * FROM news_articles WHERE is_hidden = 1 ORDER BY published_at DESC"
        rows = self.fetchall(query)
        return [dict(row) for row in rows]


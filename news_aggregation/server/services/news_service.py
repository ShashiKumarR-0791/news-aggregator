from datetime import datetime, timedelta, timezone
from server.models.news_article import NewsArticle
from server.repositories.news_repository import NewsRepository
from server.repositories.category_repository import CategoryRepository

class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.category_repo = CategoryRepository()

    def add_article(self, article_data):
        article = NewsArticle(
            title=article_data['title'],
            description=article_data.get('description'),
            content=article_data.get('content'),
            url=article_data['url'],
            source=article_data['source'],
            category_id=article_data.get('category_id'),
            published_at=article_data.get('published_at', datetime.utcnow().isoformat()),
        )
        self.news_repo.add_news(article)

    def get_today_articles(self):
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        return self.news_repo.get_news_by_date(today)

    def get_articles_by_date_range(self, start_date, end_date):
        return self.news_repo.get_news_by_range(start_date, end_date)

    def get_articles_by_category_and_date(self, category_name, date_str):
        categories = self.category_repo.get_all_categories()
        cat_id = next((c['category_id'] for c in categories if c['name'].lower() == category_name.lower()), None)
        if not cat_id:
            return []
        return self.news_repo.get_news_by_date_and_category(date_str, cat_id)


    def get_last_24_hours_articles(self):
        since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        query = "SELECT * FROM news_articles WHERE published_at >= ? ORDER BY published_at DESC"
        rows = self.news_repo.fetchall(query, (since,))
        return [dict(row) for row in rows]

    def get_recent_articles(self, hours=24):
        since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        print(f"🔍 Filtering articles since: {since}")
        query = "SELECT * FROM news_articles WHERE published_at >= ? ORDER BY published_at DESC"
        rows = self.news_repo.fetchall(query, (since,))
        print(f"📦 Found {len(rows)} articles in last {hours} hours")
        return [dict(row) for row in rows]


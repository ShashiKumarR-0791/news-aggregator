from datetime import datetime, timedelta, timezone
from server.models.news_article import NewsArticle
from server.repositories.news_repository import NewsRepository
from server.repositories.category_repository import CategoryRepository

class NewsService:
    CATEGORY_KEYWORDS = {
    "business": ["business", "market", "stock", "company", "finance", "investment", "economy"],
    "sports": ["sport", "football", "cricket", "match", "goal", "team", "tournament"],
    "technology": ["tech", "ai", "software", "app", "robot", "gadget", "device", "nasa"],
    "entertainment": ["movie", "film", "celebrity", "series", "tv", "show", "music", "award"],
    }
    def infer_category_id(self, text):
        text = (text or "").lower()
        for category_name, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return self.category_repo.get_category_id_by_name(category_name)
        return None


    def __init__(self):
        self.news_repo = NewsRepository()
        self.category_repo = CategoryRepository()
    def add_article(self, article_data):
        category_id = article_data.get('category_id')

        if not category_id:
            text_to_check = f"{article_data.get('title', '')} {article_data.get('description', '')}"
            category_id = self.infer_category_id(text_to_check)

        article = NewsArticle(
            title=article_data['title'],
            description=article_data.get('description'),
            content=article_data.get('content'),
            url=article_data['url'],
            source=article_data['source'],
            category_id=category_id,
            published_at=article_data.get('published_at', datetime.utcnow().isoformat()),
        )
        self.news_repo.add_news(article)

    # def add_article(self, article_data):
    #     article = NewsArticle(
    #         title=article_data['title'],
    #         description=article_data.get('description'),
    #         content=article_data.get('content'),
    #         url=article_data['url'],
    #         source=article_data['source'],
    #         category_id=article_data.get('category_id'),
    #         published_at=article_data.get('published_at', datetime.utcnow().isoformat()),
    #     )
    #     self.news_repo.add_news(article)

    def get_today_articles(self, category_name=None):
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        articles = self.news_repo.get_news_by_date(today)
        
        if category_name:
            category_id = self.category_repo.get_category_id_by_name(category_name)
            if not category_id:
                return []
            articles = [a for a in articles if a['category_id'] == category_id]
        return articles


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
        print(f" Found {len(rows)} articles in last {hours} hours")
        return [dict(row) for row in rows]
    def search_articles(self, query, start_date, end_date):
        query = query.lower()
        articles = self.news_repo.get_news_by_range(start_date, end_date)
        filtered = [
            a for a in articles
            if query in a['title'].lower()
            or query in (a.get('description') or '').lower()
            or query in (a.get('content') or '').lower()
        ]
        sorted_articles = sorted(
            filtered,
            key=lambda a: (a.get("likes", 0) - a.get("dislikes", 0)),
            reverse=True
        )
        return sorted_articles

    def search_news(self, keyword, start_date=None, end_date=None):
        return self.news_repo.search_articles(keyword, start_date, end_date)




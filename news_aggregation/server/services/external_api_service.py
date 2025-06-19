import json
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs

from server.services.news_service import NewsService
from server.services.notification_service import NotificationService
from server.repositories.external_server_repository import ExternalServerRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.user_repository import UserRepository
from server.utils.email_helper import send_email

class ExternalAPIService:
    def __init__(self):
        self.external_repo = ExternalServerRepository()
        self.news_service = NewsService()
        self.category_repo = CategoryRepository()
        self.notification_service = NotificationService()
        self.user_repo = UserRepository()

    def infer_category(self, text):
        CATEGORY_KEYWORDS = {
            "business": ["business", "market", "stock", "economy", "company", "finance", "investment"],
            "sports": ["sport", "football", "cricket", "match", "goal", "tournament", "team"],
            "technology": ["tech", "ai", "gadget", "software", "robot", "device"],
            "entertainment": ["movie", "film", "music", "tv", "show", "award", "series", "celebrity"],
        }
        text = (text or "").lower()

        for name, keywords in CATEGORY_KEYWORDS.items():
            if any(word in text for word in keywords):
                return name
        return "general"

    def fetch_and_store_all(self):
        servers = self.external_repo.get_all_servers(with_api_keys=True)
        for server in servers:
            print(f"\n📡 Fetching from: {server['name']}")
            articles = self.fetch_articles(server)
            print(f" {len(articles)} articles fetched from {server['name']}")

            for article in articles:
                try:
                    if not isinstance(article, dict):
                        print(f"⚠️ Skipping invalid article format: {article}")
                        continue

                    title = article.get('title')
                    if not title:
                        continue

                    source = article.get('source', {}).get('name') if isinstance(article.get('source'), dict) else article.get('source') or 'Unknown'
                    published_at = article.get('publishedAt') or article.get('published_at') or datetime.now(timezone.utc).isoformat()

                    # Determine category
                    if server['name'] == "NewsAPI":
                        parsed = parse_qs(urlparse(server['api_url']).query)
                        category_name = parsed.get("category", ["general"])[0].lower()
                    elif server['name'] == "TheNewsAPI":
                        categories = article.get("categories")
                        if isinstance(categories, list) and categories:
                            category_name = categories[0].lower()
                        else:
                            combined_text = f"{title} {article.get('description', '')}"
                            category_name = self.infer_category(combined_text)
                    else:
                        combined_text = f"{title} {article.get('description', '')}"
                        category_name = self.infer_category(combined_text)

                    category_id = self.category_repo.get_category_id_by_name(category_name)
                    if not category_id:
                        self.category_repo.add_category(category_name)
                        category_id = self.category_repo.get_category_id_by_name(category_name)

                    print(f"📝 Saving article: {title[:60]} [Category: {category_name} → ID: {category_id}]")

                    article_data = {
                        'title': title,
                        'description': article.get('description'),
                        'content': article.get('content', ''),
                        'url': article.get('url'),
                        'source': source,
                        'published_at': published_at,
                        'category_id': category_id,
                        'category': category_name
                    }

                    self.news_service.add_article(article_data)

                    # 🚨 Notify matching users
                    users = self.user_repo.get_all_users()
                    for user in users:
                        user_id = user["user_id"]
                        configs = self.notification_service.get_user_config(user_id)
                        for config in configs:
                            if config["is_enabled"] and config["category"].lower() == category_name:
                                message = f"📰 New article in your subscribed category '{category_name}': {title}"
                                self.notification_service.send_notification(user_id, message)
                                send_email(user["email"], "🗞️ News Alert", message)

                except Exception as e:
                    print(f" Failed to save article: {e}")

    def fetch_articles(self, server):
        url = server['api_url']
        name = server['name']

        if name == "NewsAPI":
            headers = {"X-Api-Key": server["api_key"]}
        elif name == "TheNewsAPI":
            headers = {"Authorization": f"Bearer {server['api_key']}"}
        else:
            headers = {}

        print(f"➡️ Requesting: {url}")
        print(f"🗝️ Using API Key: {server['api_key'][:6]}...")

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.load(response)
                print(f"📥 Raw response preview: {json.dumps(data)[:250]}...\n")

                return (
                    data.get("articles") or
                    data.get("news") or
                    data.get("data") or []
                )

        except Exception as e:
            print(f" API Fetch Error: {e}")
            return []

import threading
import time
from server.services.external_api_service import ExternalAPIService
from server.services.notification_service import NotificationService
from server.services.news_service import NewsService
from server.services.email_service import EmailService
from server.repositories.user_repository import UserRepository

class BackgroundScheduler:
    def __init__(self, interval_hours=3):
        self.interval = interval_hours * 3600  
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.running = True

        self.external_api = ExternalAPIService()
        self.notification_service = NotificationService()
        self.email_service = EmailService()
        self.news_service = NewsService()
        self.user_repo = UserRepository()

    def start(self):
        print(" Background scheduler started")
        self.thread.start()

    def run(self):
        while self.running:
            print("Background task: Fetching news & sending notifications...")
            self.external_api.fetch_and_store_all()

            all_users = self.user_repo.get_all_users()
            today_articles = self.news_service.get_today_articles()

            for user in all_users:
                uid = user["user_id"]
                email = user["email"]
                for article in today_articles:
                    article_text = f"{article.get('title')} {article.get('description')} {article.get('content')}"
                    if self.notification_service.check_keywords_in_article(uid, article_text):
                        msg = f"Matched keyword alert!\n{article.get('title')}\nURL: {article.get('url')}"
                        self.notification_service.send_notification(uid, msg, "keyword")
                        self.email_service.send_email(email, "News Keyword Alert", msg)

            time.sleep(self.interval)

    def stop(self):
        self.running = False

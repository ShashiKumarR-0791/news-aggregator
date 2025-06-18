from server.models.notification import Notification
from server.models.notification_config import NotificationConfig
from server.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    def send_notification(self, user_id, message, notif_type='info'):
        notif = Notification(user_id=user_id, message=message, type=notif_type)
        self.repo.add_notification(notif)

    def get_user_notifications(self, user_id):
        return self.repo.get_notifications_by_user(user_id)

    def configure_user_notifications(self, user_id, category, is_enabled=True, keywords=''):
        config = NotificationConfig(user_id, category, is_enabled, keywords)
        self.repo.save_config(config)

    def get_user_config(self, user_id):
        return self.repo.get_config_by_user(user_id)

    def check_keywords_in_article(self, user_id, article_text):
        configs = self.repo.get_config_by_user(user_id)
        keyword_config = next((c for c in configs if c['category'].lower() == 'keywords'), None)
        if keyword_config and keyword_config['is_enabled']:
            keywords = (keyword_config['keywords'] or '').lower().split(',')
            return any(kw.strip() in article_text.lower() for kw in keywords)
        return False

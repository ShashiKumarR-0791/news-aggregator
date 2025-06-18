from server.repositories.base_repository import BaseRepository
from server.models.notification import Notification
from server.models.notification_config import NotificationConfig

class NotificationRepository(BaseRepository):
    def add_notification(self, notif: Notification):
        query = '''
            INSERT INTO notifications (user_id, message, type, is_read, created_at)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            notif.user_id,
            notif.message,
            notif.type,
            int(notif.is_read),
            notif.created_at
        ))

    def get_notifications_by_user(self, user_id):
        query = 'SELECT * FROM notifications WHERE user_id = ?'
        rows = self.fetchall(query, (user_id,))
        return [dict(row) for row in rows]

    def save_config(self, config: NotificationConfig):
        query = '''
            INSERT OR REPLACE INTO notification_configs (user_id, category, is_enabled, keywords, created_at)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            config.user_id,
            config.category,
            int(config.is_enabled),
            config.keywords,
            config.created_at
        ))

    def get_config_by_user(self, user_id):
        query = 'SELECT * FROM notification_configs WHERE user_id = ?'
        rows = self.fetchall(query, (user_id,))
        return [dict(row) for row in rows]

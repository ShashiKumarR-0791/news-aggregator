from server.services.notification_service import NotificationService

notif_service = NotificationService()

def view_notifications(data, _):
    user_id = data.get("user_id")
    return notif_service.get_user_notifications(user_id)

def configure_notifications(data, _):
    user_id = data.get("user_id")
    category = data.get("category")
    is_enabled = data.get("is_enabled", True)
    keywords = data.get("keywords", "")
    notif_service.configure_user_notifications(user_id, category, is_enabled, keywords)
    return {"message": "Notification config updated."}

def get_configs(data, _):
    user_id = data.get("user_id")
    return notif_service.get_user_config(user_id)

from server.services.notification_service import NotificationService

notif_service = NotificationService()

# === OLD (if still used anywhere) ===
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

# === REST-STYLE used by client/api/notification_api.py ===

def get_notifications_handler(_, user):
    notifications = notif_service.get_notifications(user['user_id'])
    return {"notifications": notifications}

def get_configs_handler(_, user):
    configs = notif_service.get_user_config(user['user_id'])
    return {"configs": configs}

def configure_notification_handler(data, user):
    category = data.get("category")
    is_enabled = data.get("is_enabled", True)
    notif_service.configure_user_notifications(user['user_id'], category, is_enabled)
    return {"message": "Notification config updated."}

def update_keywords_handler(data, user):
    keywords = data.get("keywords", "")
    notif_service.update_keywords(user['user_id'], keywords)
    return {"message": "Keywords updated."}

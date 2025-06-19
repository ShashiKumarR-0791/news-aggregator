from client.api import news_api
from server.utils.router import Router
from server.utils.http_server import run_server
from server.controllers import (
    auth_controller,
    news_controller,
    external_api_controller,
    user_controller,
    notification_controller
)
from server.services.background_scheduler import BackgroundScheduler

def setup_routes():
    router = Router()

    # ✅ Create controller instances
    user_ctrl = user_controller.UserController()

    # 🔐 Auth routes
    router.add_route("POST", "/signup", auth_controller.signup_handler)
    router.add_route("POST", "/login", auth_controller.login_handler)
    router.add_route("DELETE", "/admin/delete-user", user_ctrl.delete_user)
    router.add_route("POST", "/admin/promote-user", user_ctrl.promote_user)

    # 📰 News routes
    router.add_route("GET", "/news/today", news_controller.get_today_news_handler)
    router.add_route("POST", "/news/range", news_controller.get_range_news_handler)
    router.add_route("POST", "/news/by-category", news_controller.get_news_by_category_handler)
    router.add_route("POST", "/news/today-by-category", news_controller.get_today_news_by_category_handler)
    router.add_route("POST", "/news/search", news_controller.search_news_handler)
    router.add_route("POST", "/news/like", news_controller.like_article_handler)
    router.add_route("POST", "/news/dislike", news_controller.dislike_article_handler)


    user_ctrl = user_controller.UserController()

    router.add_route("POST", "/saved", user_ctrl.save_article)
    router.add_route("POST", "/user/save-article", user_ctrl.save_article)



    # 🌍 External API fetch
    router.add_route("POST", "/external/fetch", external_api_controller.fetch_news_handler)

    # 💾 Saved Articles (using user_ctrl instance methods)
    router.add_route("POST", "/user/save-article", user_ctrl.save_article)
    router.add_route("POST", "/user/saved", user_ctrl.get_saved_articles)
    router.add_route("DELETE", "/user/delete-article", user_ctrl.delete_saved_article)

    # 🔔 Notifications
    router.add_route("GET", "/notifications", notification_controller.get_notifications_handler)
    router.add_route("GET", "/notifications/config", notification_controller.get_configs_handler)
    router.add_route("POST", "/notifications/config/update", notification_controller.configure_notification_handler)
    router.add_route("POST", "/notifications/config/keywords", notification_controller.update_keywords_handler)

    return router

if __name__ == "__main__":
    scheduler = BackgroundScheduler(interval_hours=3)
    scheduler.start()

    router = setup_routes()
    run_server(router)

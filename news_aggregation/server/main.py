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

    # 🔐 Auth routes
    router.add_route("POST", "/signup", auth_controller.signup_handler)
    router.add_route("POST", "/login", auth_controller.login_handler)

    # 📰 News routes
    router.add_route("GET", "/news/today", news_controller.get_today_news_handler)
    router.add_route("POST", "/news/range", news_controller.get_range_news_handler)
    router.add_route("POST", "/news/by-category", news_controller.get_news_by_category_handler)

    # 🌍 External API fetch
    router.add_route("POST", "/external/fetch", external_api_controller.fetch_news_handler)

    # 💾 Saved Articles
    router.add_route("POST", "/user/save-article", user_controller.UserController.save_article)
    router.add_route("DELETE", "/user/delete-article", user_controller.UserController.delete_saved_article)
    router.add_route("POST", "/user/saved", user_controller.UserController.get_saved_articles)

    # 🔔 Notifications
    router.add_route("POST", "/notifications/view", notification_controller.view_notifications)
    router.add_route("POST", "/notifications/configure", notification_controller.configure_notifications)
    router.add_route("POST", "/notifications/configs", notification_controller.get_configs)

    return router

if __name__ == "__main__":
    # Start background task
    scheduler = BackgroundScheduler(interval_hours=3)
    scheduler.start()

    # Start API server
    router = setup_routes()
    run_server(router)

from server.services.news_service import NewsService
from server.utils.response import json_response, error_response

news_service = NewsService()

def get_today_news_handler(_, __):
    return news_service.get_recent_articles(hours=48)

def get_range_news_handler(data, _):
    start = data.get('start_date')
    end = data.get('end_date')
    return news_service.get_articles_by_date_range(start, end)

def get_news_by_category_handler(data, _):
    category = data.get('category')
    date = data.get('date')
    return news_service.get_articles_by_category_and_date(category, date)

def get_today_news_by_category_handler(request, body):
    category = body.get("category")
    from server.services.news_service import NewsService
    service = NewsService()
    articles = service.get_today_articles(category)
    return {
        "status": "success",
        "articles": articles
    }

def search_news_handler(request, data):  
    keyword = data.get("query", "").lower()
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    return news_service.search_news(keyword, start_date, end_date)


def get_today_by_category_handler(data, _):
    category = data.get("category")
    return news_service.get_today_articles(category)
from server.repositories.news_repository import NewsRepository

repo = NewsRepository()

def like_article_handler(request,user=None):
    try:
        article_id = request.get("article_id")
        if not article_id:
            return {"error": "article_id is required"}, 400

        repo.increment_like(article_id)
        return {"message": "Article liked"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


def dislike_article_handler(request,user=None):
    try:
        article_id = request.get("article_id")
        if not article_id:
            return {"error": "article_id is required"}, 400

        repo.increment_dislike(article_id)
        return {"message": "Article disliked"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

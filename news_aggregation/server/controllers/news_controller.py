from server.services.news_service import NewsService
from server.utils.response import json_response, error_response

news_service = NewsService()

def get_today_news_handler(_, __):
    return news_service.get_recent_articles(hours=48)

def get_range_news_handler(data, _):
    start = data.get('start_date')
    end = data.get('end_date')
    articles = news_service.get_articles_by_date_range(start, end)
    return {"articles": articles}


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




def get_today_by_category_handler(data, _):
    category = data.get("category")
    return news_service.get_today_articles(category)
from server.repositories.news_repository import NewsRepository

repo = NewsRepository()

def like_article_handler(request, user=None):
    try:
        article_id = request.get("article_id")
        if not article_id:
            return {"error": "article_id is required", "status": 400}

        repo.increment_like(article_id)
        return {"message": "Article liked", "status": 200}
    except Exception as e:
        return {"error": str(e), "status": 500}


def dislike_article_handler(request, user=None):
    try:
        article_id = request.get("article_id")
        if not article_id:
            return {"error": "article_id is required", "status": 400}

        repo.increment_dislike(article_id)
        return {"message": "Article disliked", "status": 200}
    except Exception as e:
        return {"error": str(e), "status": 500}
    
def search_news_handler(data, _user):
    try:
        keyword = data.get("keyword", "").strip()
        start = data.get("start_date")
        end = data.get("end_date")

        if not keyword:
            return {"error": "Keyword is required", "status": 400}

        results = repo.search_articles_by_keyword(keyword, start, end)
        return {"results": results, "status": 200}
    except Exception as e:
        return {"error": str(e), "status": 500}
def report_article_handler(request, user):
    try:
        article_id = request.get("article_id")
        if not article_id:
            return {"error": "article_id is required", "status": 400}
        from server.repositories.news_repository import NewsRepository
        repo = NewsRepository()
        report_count = repo.add_report(article_id)
        message = f"Article reported successfully. Total reports: {report_count}"
        if report_count >= 3:
            message += " (Article has been hidden due to multiple reports)"
        return {"message": message, "report_count": report_count, "status": 200}
    except Exception as e:
        print(f"DEBUG: Exception in report_article_handler: {e}")
        return {"error": str(e), "status": 500}
    
def get_reported_articles_handler(_request, user):
    if user.get("role") != "admin":
        return {"error": "Unauthorized", "status": 403}

    from server.repositories.news_repository import NewsRepository
    repo = NewsRepository()
    articles = repo.get_reported_articles()
    print("******************")
    print("DEBUG: Reported articles returned to admin:", articles)
    return {"articles": articles, "status": 200}

def delete_article_handler(request, user):
    if user.get("role") != "admin":
        return {"error": "Unauthorized", "status": 403}

    article_id = request.get("article_id")
    if not article_id:
        return {"error": "Missing article_id", "status": 400}

    from server.repositories.news_repository import NewsRepository
    repo = NewsRepository()
    
    if repo.delete_article(article_id):
        return {"message": "Article deleted successfully", "status": 200}
    else:
        return {"error": "Failed to delete article", "status": 500}




def unhide_article_handler(request, user):
    if not user or user.get("role") != "admin":
        return {"error": "Unauthorized", "status": 403}

    article_id = request.get("article_id")
    if not article_id:
        return {"error": "Missing article_id", "status": 400}

    from server.repositories.news_repository import NewsRepository
    repo = NewsRepository()
    repo.unhide_article(article_id)
    return {"message": "Article unhidden successfully", "status": 200}

def get_most_liked_articles_handler(request, user):
    try:
        limit = request.get("limit", 20)
        from server.repositories.news_repository import NewsRepository
        repo = NewsRepository()
        articles = repo.get_most_liked_articles(limit)
        return {"articles": articles, "status": 200}
    except Exception as e:
        return {"error": str(e), "status": 500}

def get_hidden_articles_handler(_request, user):
    if user.get("role") != "admin":
        return {"error": "Unauthorized", "status": 403}
    articles = repo.get_hidden_articles()
    return {"articles": articles, "status": 200}


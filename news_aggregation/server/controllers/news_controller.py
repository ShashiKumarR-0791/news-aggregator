from server.services.news_service import NewsService

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

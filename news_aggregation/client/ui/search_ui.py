from client.api.news_api import search_articles
from client.ui.article_ui import display_articles, save_article_prompt
from client.session import session
from datetime import datetime

def show_search_menu(user):
    import requests
    from client.session import session

    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print(" Keyword is required.")
        return

    start_date = input("Start Date (YYYY-MM-DD) [optional]: ").strip()
    end_date = input("End Date (YYYY-MM-DD) [optional]: ").strip()

    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    if start_date and not is_valid_date(start_date):
        print(" Invalid start date format. Please use YYYY-MM-DD.")
        return
    if end_date and not is_valid_date(end_date):
        print(" Invalid end date format. Please use YYYY-MM-DD.")
        return

    payload = {"keyword": keyword}
    if start_date:
        payload["start_date"] = start_date
    if end_date:
        payload["end_date"] = end_date

    try:
        response = requests.post(
            "http://localhost:8000/news/search",
            json=payload,
            headers=session.get_headers()
        )
        try:
            data = response.json()
        except Exception:
            try:
                data = eval(response.text) 
            except Exception as e:
                print(" Cannot parse server response:", e)
                return

        print("🔍 RAW SEARCH RESPONSE:", data)

        articles = data.get("results", [])

        print(f"\nWelcome to the News Application, {user['username']}! Search Results for “{keyword}”")
        if not articles:
            print(" No results found.")
            return

        for idx, article in enumerate(articles, 1):
            print(f"\n{idx}. {article['title']}")
            print(f"    Source      : {article['source']}")
            print(f"    Published At: {article['published_at']}")
            print(f"    URL         : {article['url']}")
    except Exception as e:
        print(f" Failed to fetch search results: {e}")

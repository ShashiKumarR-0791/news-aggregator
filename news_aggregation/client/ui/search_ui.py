from client.api.news_api import search_articles
from client.ui.article_ui import display_articles, save_article_prompt
from client.session import session

def show_search_menu(user):  
    query = input("Enter search keyword: ").strip().lower()
    start = input("Start Date (YYYY-MM-DD): ").strip()
    end = input("End Date (YYYY-MM-DD): ").strip()
    
    results = search_articles(query, start, end)
    print(f"\nWelcome to the News Application, {user['username']}! Search Results for “{query}”")

    if not results:
        print(" No results found.")
        return

    for article in results:
        print(f"\n {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published At: {article['published_at']}")
        print(f"URL: {article['url']}")
        # print(f"Category: {article.get('category', 'N/A')}")
        print(f"Article Id: {article['article_id']}")


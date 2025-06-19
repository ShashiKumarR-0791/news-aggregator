from client.api.news_api import get_today_news,get_news_by_date_range, get_today_news_by_category
from client.ui.article_ui import display_articles, save_article_prompt

def show_headlines_menu(user):
    while True:
        print("\nHeadlines:")
        print("1. Today")
        print("2. Date range")
        print("3. Logout")
        choice = input("Choose: ").strip()

        if choice == '1':
            show_today_category_menu()
        elif choice == '2':
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            articles = get_news_by_date_range( start, end)
            display_articles(articles)
            save_article_prompt()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

def show_today_category_menu():
    category_map = {
        "1": "all",
        "2": "business",
        "3": "entertainment",
        "4": "sports",
        "5": "technology"
    }

    print("\nPlease choose the options below for Headlines")
    print("1. All")
    print("2. Business")
    print("3. Entertainment")
    print("4. Sports")
    print("5. Technology")
    print("6. Back")

    choice = input("Choose: ").strip()
    if choice == "6":
        return

    category = category_map.get(choice)
    if category:
        from client.api.news_api import get_today_news_by_category
        articles = get_today_news_by_category(category)

        if isinstance(articles, list):
            display_articles(articles)
        else:
            print("Failed to load articles:", articles)
    else:
        print(" Invalid choice.")

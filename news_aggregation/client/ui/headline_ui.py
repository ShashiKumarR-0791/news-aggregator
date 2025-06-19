from client.api.news_api import (
    get_today_news_by_category,
    get_news_by_date_range
)
from client.ui.article_ui import (
    display_articles,
    save_article_prompt
)

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
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()

            response = get_news_by_date_range(start_date, end_date)
            articles = response.get("articles") if isinstance(response, dict) else None

            if articles:
                display_articles(articles)
                save_article_prompt()
            else:
                print("❌ Failed to fetch articles:", response)
        elif choice == '3':
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def show_today_category_menu():
    category_map = {
        "1": "all",
        "2": "business",
        "3": "entertainment",
        "4": "sports",
        "5": "technology"
    }

    while True:
        print("\nPlease choose the options below for Headlines")
        print("1. All")
        print("2. Business")
        print("3. Entertainment")
        print("4. Sports")
        print("5. Technology")
        print("6. Back")
        choice = input("Choose: ").strip()

        if choice == "6":
            break

        category = category_map.get(choice)
        if category:
            response = get_today_news_by_category(category)
            articles = response.get("articles") if isinstance(response, dict) else None

            if articles:
                display_articles(articles)
                save_article_prompt()
            else:
                print("❌ Failed to load articles:", response)
        else:
            print("❌ Invalid choice. Please select from 1 to 6.")

from client.services.api_client import APIClient
from client.services.session_manager import SessionManager

api = APIClient()
session = SessionManager()
from client.api.saved_api import get_saved_articles, delete_article
from client.session import session

def show_saved_menu():
    user = session.get_user()
    if not user:
        print("❌ No user in session. Please log in again.")
        return

    while True:
        articles = get_saved_articles(user['user_id'])

        if not articles:
            print("❌ No saved articles.")
            return

        print(f"\n📚 Saved Articles for {user['username']}:")
        for idx, article in enumerate(articles, 1):
            print(f"\n{idx}. 📰 {article['title']}")
            print(f"    Source    : {article['source']}")
            print(f"    URL       : {article['url']}")
            print(f"    Article ID: {article['article_id']}")
            print(f"    Category  : {article.get('category', 'N/A')}")

        print("\n1. Back\n2. Logout\n3. Delete Article")
        choice = input("Choose: ").strip()

        if choice == '1':
            break
        elif choice == '2':
            session.logout()
            print("Logged out.")
            exit()
        elif choice == '3':
            try:
                aid = int(input("Enter Article ID to delete: ").strip())
                success = delete_article(user['user_id'], aid)
                if success:
                    print("✅ Article deleted.")
                else:
                    print("❌ Failed to delete article.")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Invalid choice.")


def print_articles(response):
    print("📤 Received response from API:", response) 

    if "error" in response:
        print("", response["error"])
        return
    if not response:
        print("No articles found.")
        return
    for article in response:
        print(f"\n {article['title']}")
        print(f"  Source: {article['source']}")
        print(f"  Published At: {article['published_at']}")
        print(f"  URL: {article['url']}")

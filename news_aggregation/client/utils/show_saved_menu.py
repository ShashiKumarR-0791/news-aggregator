from client.services.api_client import APIClient
from client.services.session_manager import SessionManager

api = APIClient()
session = SessionManager()
from client.api.saved_api import get_saved_articles, delete_article
from client.session import session

def show_saved_menu():
    user = session.get_user()
    user_id = user['user_id'] if user and 'user_id' in user else None
    username = user['username'] if user and 'username' in user else 'User'

    if not user_id:
        print(" No user in session. Showing saved articles is limited.")
        articles = []
    else:
        articles = get_saved_articles(user_id)

    if not articles:
        print(" No saved articles.")
        return

    print(f"\n📚 Saved Articles for {username}:")
    for idx, article in enumerate(articles, 1):
        print(f"\n{idx}.  {article['title']}")
        print(f"    Source    : {article['source']}")
        print(f"    URL       : {article['url']}")
        print(f"    Article ID: {article['article_id']}")
        print(f"    Category  : {article.get('category', 'N/A')}")

    print("\n1. Back\n2. Logout\n3. Delete Article")
    choice = input("Choose: ").strip()

    if choice == '1':
        return
    elif choice == '2':
        session.logout()
        print("Logged out.")
        exit()
    elif choice == '3':
        try:
            aid = int(input("Enter Article ID to delete: ").strip())
            if not user_id:
                print(" Cannot delete without user session.")
                return
            success = delete_article(user_id, aid)
            if success:
                print(" Article deleted.")
            else:
                print(" Failed to delete article.")
        except Exception as e:
            print(f" Error: {e}")
    else:
        print(" Invalid choice.")


def print_articles(response):
    print(" Received response from API:", response) 

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

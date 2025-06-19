from client.api.saved_api import get_saved_articles, delete_article
from client.session import session

def show_saved_menu():
    user = session.get_user()
    if not user:
        print("❌ No user in session. Please log in again.")
        return

    articles = get_saved_articles(user['user_id'])

    if not articles:
        print("❌ No saved articles.")
        return

    print(f"\nWelcome to the News Application, {user['username']}! Your Saved Articles:")

    for article in articles:
        print(f"\n📰 Article Id: {article['article_id']} - {article['title']}")
        print(f"{article['description']}\nSource: {article['source']}")
        print(f"URL: {article['url']}")
        print(f"Category: {article.get('category', 'N/A')}")

    while True:
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
                aid = int(input("Enter Article Id to delete: "))
                success = delete_article(user['user_id'], aid)
                if success:
                    print("✅ Article deleted.")
                else:
                    print("❌ Failed to delete article.")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("Invalid choice.")
from client.api.saved_api import get_saved_articles
from client.session import session

def show_saved_articles():
    if not session.is_authenticated():
        print("❌ No user in session. Please log in again.")
        return

    articles = get_saved_articles()
    if not articles:
        print("❌ No saved articles found.")
        return

    print("\n--- 📚 Saved Articles ---")
    for idx, article in enumerate(articles, 1):
        print(f"\n{idx}. {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published At: {article['published_at']}")
        print(f"URL: {article['url']}")

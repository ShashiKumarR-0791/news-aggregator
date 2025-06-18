
from client.services.api_client import APIClient
from client.services.session_manager import SessionManager

api = APIClient()
session = SessionManager()
def show_saved_menu():
    while True:
        print("\n--- Saved Articles ---")
        print("1. View")
        print("2. Delete Article")
        print("3. Back")
        choice = input("Choose: ")
        if choice == '1':
            response = api.request("POST", "/user/saved", {"user_id": session.get_user_id()})
            print_articles(response)
        elif choice == '2':
            aid = input("Article ID to remove: ")
            response = api.request("DELETE", "/user/delete-article", {
                "user_id": session.get_user_id(),
                "article_id": aid
            })
            print(response.get("message") or response.get("error"))
        elif choice == '3':
            break

def print_articles(response):
    print("📤 Received response from API:", response)  # ← ADD THIS

    if "error" in response:
        print("❌", response["error"])
        return
    if not response:
        print("No articles found.")
        return
    for article in response:
        print(f"\n📰 {article['title']}")
        print(f"  Source: {article['source']}")
        print(f"  Published At: {article['published_at']}")
        print(f"  URL: {article['url']}")

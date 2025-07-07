from client.api.saved_api import save_article
from client.session import session

def display_articles(articles):
    if not articles:
        print("No articles found.")
        return

    print("\n--- Articles ---")

    for index, article in enumerate(articles, start=1):
        print(f"\n{index}. {article.get('title', 'No Title')}")
        print(f"    Source      : {article.get('source', 'Unknown')}")
        print(f"   📅 Published At: {article.get('published_at', 'Unknown')}")
        print(f"   🔗 URL         : {article.get('url', 'N/A')}")
        print(f"   🆔 Article ID  : {article.get('article_id', 'N/A')}")



def save_article_prompt():
    while True:
        print("\n1. Back\n2. Logout\n3. Save Article")
        choice = input("Choose: ").strip()
        if choice == '1':
            break
        elif choice == '2':
            session.clear()
            print("Logged out.")
            exit()
        elif choice == '3':
            try:
                aid = int(input("Article Id: "))
                save_article(aid)
            except:
                print("Invalid ID.")
        else:
            print("Invalid choice.")

from client.api.saved_api import save_article
from client.session import session

def display_articles(articles):
    if not articles:
        print("No articles found.")
        return

    for article in articles:
        print(f"\n {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published At: {article['published_at']}")
        print(f"URL: {article['url']}")
        # print(f"Category: {article.get('category') or 'N/A'}")
        print(f"Article Id: {article['article_id']}")

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

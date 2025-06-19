import json
import urllib.request
from urllib.parse import urlparse, parse_qs

NEWSAPI_KEY = "af3ce09176fb4fd3be6fcfd1e000776c"
THENEWSAPI_KEY = "E59Lzz4zfUYOtWZ3zQGV8Ofo9Vj7RcSNX02LcSet"

external_servers = [
    {
        "name": "NewsAPI",
        "url": "https://newsapi.org/v2/top-headlines?country=us&category=business",
        "headers": {"X-Api-Key": NEWSAPI_KEY}
    },
    {
        "name": "TheNewsAPI",
        "url": "https://api.thenewsapi.com/v1/news/top?locale=us&limit=10",
        "headers": {"Authorization": f"Bearer {THENEWSAPI_KEY}"}
    },
    {
        "name": "Firebase",
        "url": "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi?country=us&category=business",
        "headers": {}
    }
]

def fetch_articles(server):
    try:
        req = urllib.request.Request(server['url'], headers=server['headers'])
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = (
                data.get("articles") or
                data.get("news") or
                data.get("data") or []
            )
            return articles
    except Exception as e:
        print(f" Error fetching from {server['name']}: {e}")
        return []

def extract_categories(articles, server):
    server_name = server['name']
    categories = set()

    for article in articles:
        if not isinstance(article, dict):
            continue

        if server_name == "NewsAPI":
            parsed = parse_qs(urlparse(server["url"]).query)
            cat = parsed.get("category", ["general"])[0].lower()
            categories.add(cat)

        elif server_name == "TheNewsAPI":
            cat_field = article.get("categories")
            if isinstance(cat_field, list):
                categories.update(c.lower() for c in cat_field if isinstance(c, str))

        else:
            categories.add("general")  

    return categories

if __name__ == "__main__":
    all_categories = set()

    for server in external_servers:
        print(f"\n📡 Checking categories from {server['name']}...")
        articles = fetch_articles(server)
        found = extract_categories(articles, server)
        if found:
            print(f" Found categories: {sorted(found)}")
            all_categories.update(found)
        else:
            print("⚠️ No categories found in articles.")

    print("\n📋 All unique categories collected across APIs:")
    print(sorted(all_categories) or " None found")

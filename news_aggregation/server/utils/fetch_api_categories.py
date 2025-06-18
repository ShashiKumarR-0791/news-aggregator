# import json
# import urllib.request

# NEWSAPI_KEY = "af3ce09176fb4fd3be6fcfd1e000776c"
# THENEWSAPI_KEY = "E59Lzz4zfUYOtWZ3zQGV8Ofo9Vj7RcSNX02LcSet"

# external_servers = [
#     {
#         "name": "NewsAPI",
#         "url": "https://newsapi.org/v2/top-headlines?country=us&category=business",
#         "headers": {"X-Api-Key": NEWSAPI_KEY}
#     },
#     {
#         "name": "TheNewsAPI",
#         "url": "https://api.thenewsapi.com/v1/news/top?locale=us&limit=3",
#         "headers": {"Authorization": f"Bearer {THENEWSAPI_KEY}"}
#     },
#     {
#         "name": "Firebase",
#         "url": "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi?country=us&category=business",
#         "headers": {}
#     }
# ]

# def fetch_data(server):
#     try:
#         req = urllib.request.Request(server["url"], headers=server["headers"])
#         with urllib.request.urlopen(req) as response:
#             return json.load(response)
#     except Exception as e:
#         print(f"❌ Error fetching from {server['name']}: {e}")
#         return None

# def extract_keys(obj, prefix=''):
#     keys = set()
#     if isinstance(obj, dict):
#         for k, v in obj.items():
#             full_key = f"{prefix}.{k}" if prefix else k
#             keys.add(full_key)
#             keys |= extract_keys(v, full_key)
#     elif isinstance(obj, list):
#         for item in obj[:3]:  # Just sample first few
#             keys |= extract_keys(item, prefix)
#     return keys

# if __name__ == "__main__":
#     for server in external_servers:
#         print(f"\n📡 Inspecting {server['name']}...")
#         data = fetch_data(server)
#         if not data:
#             continue

#         articles = data.get("articles") or data.get("news") or data.get("data")
#         if not articles:
#             print("⚠️ No articles found in response.")
#             continue

#         print(f"📦 Found {len(articles)} articles. Showing keys from sample:")
#         keys = extract_keys(articles[:3])
#         for key in sorted(keys):
#             print(f"  - {key}")


import json
import urllib.request
from urllib.parse import urlparse, parse_qs

# Replace with your real keys
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
        print(f"❌ Error fetching from {server['name']}: {e}")
        return []

def extract_categories(articles, server):
    server_name = server['name']
    categories = set()

    for article in articles:
        if not isinstance(article, dict):
            continue

        if server_name == "NewsAPI":
            # Try to infer category from URL param
            parsed = parse_qs(urlparse(server["url"]).query)
            cat = parsed.get("category", ["general"])[0].lower()
            categories.add(cat)

        elif server_name == "TheNewsAPI":
            cat_field = article.get("categories")
            if isinstance(cat_field, list):
                categories.update(c.lower() for c in cat_field if isinstance(c, str))

        else:
            categories.add("general")  # default for Firebase or unknown

    return categories

if __name__ == "__main__":
    all_categories = set()

    for server in external_servers:
        print(f"\n📡 Checking categories from {server['name']}...")
        articles = fetch_articles(server)
        found = extract_categories(articles, server)
        if found:
            print(f"✅ Found categories: {sorted(found)}")
            all_categories.update(found)
        else:
            print("⚠️ No categories found in articles.")

    print("\n📋 All unique categories collected across APIs:")
    print(sorted(all_categories) or "❌ None found")

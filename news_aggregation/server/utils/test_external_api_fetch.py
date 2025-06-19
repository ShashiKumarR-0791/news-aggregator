import json
import urllib.request
from datetime import datetime, timezone

API_KEY = "af3ce09176fb4fd3be6fcfd1e000776c"
The_API_KEY="E59Lzz4zfUYOtWZ3zQGV8Ofo9Vj7RcSNX02LcSet"
external_servers = [
    {
        "name": "NewsAPI",
        "url": "https://newsapi.org/v2/top-headlines?country=us&category=business",
        "headers": {"X-Api-Key": API_KEY}
    },
    {
        "name": "TheNewsAPI",
        "url": "https://api.thenewsapi.com/v1/news/top",
        "headers": {"Authorization": f"Bearer {The_API_KEY}"}
    },
    {
        "name": "Firebase",
        "url": "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi?country=us&category=business",
        "headers": {}
    }
]

def fetch_and_print(server):
    print(f"\n📡 Fetching from: {server['name']}")
    print(f"➡️ URL: {server['url']}")

    try:
        req = urllib.request.Request(server['url'], headers=server['headers'])
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            print(f" Status: {response.status}")
            articles = (
                data.get("articles") or
                data.get("news") or
                data.get("data") or []
            )
            print(f" Total Articles: {len(articles)}")

            for a in articles[:5]:
                if not isinstance(a, dict):
                    print(f"⚠️ Skipping non-dict article: {a}")
                    continue

                title = a.get("title")
                date = a.get("publishedAt") or a.get("date")
                source = a.get("source", {}).get("name", "Unknown") if isinstance(a.get("source"), dict) else a.get("source", "Unknown")
                print(f"- {title} | {date} | {source}")

    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    for server in external_servers:
        fetch_and_print(server)

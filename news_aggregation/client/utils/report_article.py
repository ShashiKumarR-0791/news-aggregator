import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def view_reported_articles():
    try:
        response = requests.get(f"{BASE_URL}/admin/reported-articles", headers=session.get_headers())
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f" Failed to fetch reported articles: {e}")
        return

    articles = data.get("articles") if isinstance(data, dict) else data
    if not articles:
        print(" No articles reported over the threshold.")
        return

    print("\n Reported Articles (3+ reports):")
    print("-" * 70)
    for a in articles:
        try:
            print(f"🆔 {a['article_id']} | {a['title']} | Reports: {a['report_count']} | Hidden: {bool(a['is_hidden'])}")
        except KeyError as e:
            print(f" Missing key in article data: {e}")
    print("-" * 70)

    if input(" Do you want to unhide any article? (y/n): ").strip().lower() == 'y':
        aid = input("Enter Article ID to unhide: ").strip()
        if not aid.isdigit():
            print(" Invalid Article ID.")
            return
        try:
            res = requests.post(
                f"{BASE_URL}/admin/unhide-article",
                json={"article_id": int(aid)},
                headers=session.get_headers()
            )
            result = res.json()
            print(f" {result.get('message', 'Success')}" if res.ok else f" {result.get('error', 'Failed to unhide')}")
        except Exception as e:
            print(f" Failed to send unhide request: {e}")

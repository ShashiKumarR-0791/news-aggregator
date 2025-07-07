import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def get_today_news():
    response = requests.get(f"{BASE_URL}/news/today", headers=session.get_headers())
    return response.json()

def get_news_by_date_range(start_date, end_date):
    payload = {"start_date": start_date, "end_date": end_date}
    response = requests.post(f"{BASE_URL}/news/range", json=payload, headers=session.get_headers())
    return response.json()

def get_news_by_date_range_only(start_date, end_date):
    payload = {"start_date": start_date, "end_date": end_date}
    response = requests.post(f"{BASE_URL}/news/by-date", json=payload, headers=session.get_headers())
    data = response.json()
    return data.get("articles", [])

def search_articles(keyword, start_date=None, end_date=None):
    payload = {"keyword": keyword, "start_date": start_date, "end_date": end_date}
    response = requests.post(f"{BASE_URL}/news/search", json=payload, headers=session.get_headers())

    print("🔍 RAW SEARCH RESPONSE:", response.status_code, response.text)  

    return response.json()

def search_news(query, start_date=None, end_date=None):
    url = f"{BASE_URL}/news/search"
    payload = {
        "query": query,
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.post(url, json=payload, headers=session.get_headers())
    return response.json()

def get_today_news_by_category(category):
    payload = {"category": category}
    try:
        response = requests.post(
            f"{BASE_URL}/news/today-by-category",
            json=payload,
            headers=session.get_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(" Server returned invalid JSON or empty response.")
        return []
    except requests.exceptions.RequestException as e:
        print(f" Error during request: {e}")
        return []


def like_article_by_id(article_id):
    try:
        response = requests.post(
            f"{BASE_URL}/news/like",
            json={"article_id": article_id},
            headers=session.get_headers()
        )
        response.raise_for_status()

        if response.content.strip():
            return response.json()
        else:
            return {"message": "Liked successfully (no JSON returned)"}

    except Exception as e:
        print(f" Like failed: {e}")
        return None


def dislike_article_by_id(article_id):
    try:
        response = requests.post(
            f"{BASE_URL}/news/dislike",
            json={"article_id": article_id},
            headers=session.get_headers()
        )
        response.raise_for_status()

        if response.content.strip():
            return response.json()
        else:
            return {"message": "Disliked successfully (no JSON returned)"}

    except Exception as e:
        print(f" Dislike failed: {e}")
        return None

def interact_with_articles(articles, user):
    from client.api.news_api import like_article_by_id, dislike_article_by_id, report_article_by_id
    from client.api.saved_api import save_article_by_id

    if not articles:
        return

    article_map = {str(article['article_id']): article for article in articles}

    while True:
        print("\nChoose an article to interact with:")
        print("Enter the Article ID (🆔), or 'q' to quit")
        choice = input("Choice: ").strip()

        if choice.lower() == 'q':
            break

        selected_article = article_map.get(choice)
        if not selected_article:
            print(" Invalid Article ID.")
            continue

        article_id = selected_article['article_id']
        print(f"\nSelected Article: {selected_article['title']}")
        print("1. Save")
        print("2. Like")
        print("3. Dislike")
        print("4. Report")
        print("5. Back")

        action = input("Choose an action: ").strip()

        if action == '1':
            result = save_article_by_id(user, article_id)
            if isinstance(result, dict):
                print(f" {result.get('message', result.get('error', 'Saved.'))}")
            else:
                print(f" Unexpected response: {result}")
        elif action == '2':
            like_article_by_id(article_id)
            print("👍 You liked this article.")
        elif action == '3':
            dislike_article_by_id(article_id)
            print("👎 You disliked this article.")
        elif action == '4':
            result = report_article_by_id(article_id)
            if isinstance(result, dict):
                print(f" {result.get('message', result.get('error', 'No message'))}")
            else:
                print(f" Unexpected response: {result}")
        elif action == '5':
            continue
        else:
            print(" Invalid action.")

def report_article_by_id(article_id):
    try:
        payload = {"article_id": article_id}
        headers = session.get_headers()
        response = requests.post(f"{BASE_URL}/news/report", json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f" Error reporting article: {e}")
        return None

def get_most_liked_articles(limit=20):
    try:
        response = requests.get(
            f"{BASE_URL}/news/most-liked",
            headers=session.get_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f" Error fetching most liked articles: {e}")
        return {"articles": []}

def get_reported_articles():
    try:
        response = requests.get(
            f"{BASE_URL}/admin/reported-articles",
            headers=session.get_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f" Error fetching reported articles: {e}")
        return {"articles": []}

def delete_article(article_id):
    try:
        response = requests.delete(
            f"{BASE_URL}/admin/delete-article",
            json={"article_id": article_id},
            headers=session.get_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f" Error deleting article: {e}")
        return {"error": str(e)}
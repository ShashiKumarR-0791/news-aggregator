import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def get_saved_articles(user_id):
    payload = {"user_id": user_id}
    try:
        response = requests.post(f"{BASE_URL}/user/saved", json=payload, headers=session.get_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching saved articles: {e}")
        return []

def delete_article(user_id, article_id):
    try:
        response = requests.delete(
            f"{BASE_URL}/user/delete-article",
            json={"user_id": user_id, "article_id": article_id},
            headers=session.get_headers()
        )
        response.raise_for_status()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error deleting article: {e}")
        return False
def save_article(article_id):
    payload = {"article_id": article_id}
    response = requests.post(f"{BASE_URL}/saved/save", json=payload, headers=session.get_headers())
    return response.ok

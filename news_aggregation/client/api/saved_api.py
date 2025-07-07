import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def get_saved_articles():
    try:
        headers = session.get_headers()
        response = requests.post(f"{BASE_URL}/user/saved", headers=headers)
        return response.json().get("articles", [])
    except Exception as e:
        print("❌ Failed to load saved articles:", e)
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
        print(f" Error deleting article: {e}")
        return False
def save_article(article_id):
    user = session.get_user()
    if not user:
        print("❌ No user in session. Please log in again.")
        return False

    payload = {"article_id": article_id}
    try:
        response = requests.post(
            f"{BASE_URL}/user/save-article",
            json=payload,
            headers=session.get_headers()
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Error saving article: {e}")
        return False


def save_article_by_id(user_id: int, article_id: int):
    try:
        response = requests.post(
            f"{BASE_URL}/user/save-article",
            json={"user_id": user_id, "article_id": article_id},
            headers=session.get_headers()
        )
        response.raise_for_status()
        # Ensure response is valid JSON and has expected keys
        if response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        else:
            print(" Server returned non-JSON response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f" Error saving article: {e}")
        return None

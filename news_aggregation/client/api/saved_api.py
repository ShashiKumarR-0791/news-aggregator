import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def get_saved_articles():
    try:
        headers = session.get_headers()
        response = requests.post(f"{BASE_URL}/user/saved", headers=headers)
        return response.json().get("articles", [])
    except Exception as e:
        print(" Failed to load saved articles:", e)
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
        print(" No user in session. Please log in again.")
        return False

    payload = {"article_id": article_id}
    if user.get("user_id"):
        payload["user_id"] = user["user_id"]
    if user.get("email"):
        payload["email"] = user["email"]
    try:
        response = requests.post(
            f"{BASE_URL}/user/save-article",
            json=payload,
            headers=session.get_headers()
        )
        response.raise_for_status()
        if response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        else:
            print(" Server returned non-JSON response.")
            return None
    except Exception as e:
        print(f" Error saving article: {e}")
        return None


def save_article_by_id(user, article_id):
    payload = {"article_id": article_id}
    if user.get("user_id"):
        payload["user_id"] = user["user_id"]
    if user.get("email"):
        payload["email"] = user["email"]
    try:
        response = requests.post(
            f"{BASE_URL}/user/save-article",
            json=payload,
            headers=session.get_headers()
        )
        response.raise_for_status()
        if response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        else:
            print(" Server returned non-JSON response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f" Error saving article: {e}")
        return None

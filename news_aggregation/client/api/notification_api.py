import requests
from client.session import session

BASE_URL = "http://localhost:8000"

def get_notifications():
    payload = {"user_id": session.user["user_id"]}
    response = requests.post(f"{BASE_URL}/notifications/view", json=payload, headers=session.get_headers())
    response.raise_for_status()
    return response.json()

def get_config():
    payload = {"user_id": session.user["user_id"]}
    response = requests.post(f"{BASE_URL}/notifications/configs", json=payload, headers=session.get_headers())
    response.raise_for_status()
    return response.json()

def update_config(category, is_enabled):
    payload = {
        "user_id": session.user["user_id"],
        "category": category,
        "is_enabled": is_enabled
    }
    response = requests.post(f"{BASE_URL}/notifications/configure", json=payload, headers=session.get_headers())
    response.raise_for_status()
    return response.ok

def update_keywords(keywords):
    payload = {
        "user_id": session.user["user_id"],
        "keywords": keywords
    }
    response = requests.post(f"{BASE_URL}/notifications/configure", json=payload, headers=session.get_headers())
    response.raise_for_status()
    return response.ok

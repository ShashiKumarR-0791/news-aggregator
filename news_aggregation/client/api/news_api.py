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
    return response.json()



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


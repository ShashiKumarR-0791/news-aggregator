

from client.services.api_client import APIClient
from client.services.session_manager import SessionManager
from client.utils.show_saved_menu import print_articles
api = APIClient()
session = SessionManager()
def search_articles():
    print("\n--- Search Articles ---")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")
    response = api.request("POST", "/news/range", {
        "start_date": start,
        "end_date": end
    })
    print_articles(response)

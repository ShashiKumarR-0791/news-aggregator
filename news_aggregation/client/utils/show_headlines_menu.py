from client.services.api_client import APIClient
from client.services.session_manager import SessionManager
from client.utils.show_saved_menu import print_articles
api = APIClient()
session = SessionManager()
def show_headlines_menu():
    while True:
        print("\n--- Headlines ---")
        print("1. View Today's Headlines")
        print("2. View By Category and Date")
        print("3. Back")
        choice = input("Choose: ")

        if choice == '1':
            response = api.request("GET", "/news/today")
            print_articles(response)
        elif choice == '2':
            category = input("Category (business/sports/technology/entertainment): ")
            date = input("Date (YYYY-MM-DD): ")
            response = api.request("POST", "/news/by-category", {
                "category": category,
                "date": date
            })
            print_articles(response)
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

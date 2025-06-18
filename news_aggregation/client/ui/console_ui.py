from client.services.api_client import APIClient
from client.services.session_manager import SessionManager
from client.utils import show_notification_menu, show_saved_menu
from server.controllers.category_controller import CategoryController
from server.controllers.external_server_controller import ExternalServerController

api = APIClient()
session = SessionManager()

def show_main_menu():
    while True:
        print("\n--- News Aggregator ---")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == '1':
            login()
        elif choice == '2':
            signup()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

def login():
    email = input("Email: ")
    password = input("Password: ")
    response = api.request("POST", "/login", {"email": email, "password": password})
    if response.get("success"):
        session.login(response["user"])
        print(f"Welcome {response['user']['username']}!")
        show_dashboard()
    else:
        print("❌", response.get("message") or response.get("error"))

def signup():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    role = input("Role (admin/user): ").strip().lower()
    response = api.request("POST", "/signup", {
        "username": username,
        "email": email,
        "password": password,
        "role": role if role in ['admin', 'user'] else 'user'
    })
    print("✅" if response.get("success") else "❌", response.get("message") or response.get("error"))

def show_dashboard():
    if session.get_role() == 'admin':
        show_admin_menu()
    else:
        show_user_menu()

from server.controllers.external_server_controller import ExternalServerController

external_controller = ExternalServerController()

def show_admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View External Servers Status")
        print("2. View External Server Details")
        print("3. Update External Server API Key")
        print("4. Add News Category")
        print("5. Logout")
        choice = input("Choose: ")

        if choice == '1':
            servers = external_controller.view_server_status()
            for s in servers:
                status = "Active" if s["is_active"] else "Not Active"
                print(f"{s['server_id']}. {s['name']} - {status} - Last Accessed: {s['last_accessed']}")
        elif choice == '2':
            servers = external_controller.view_server_details()
            for s in servers:
                print(f"{s['server_id']}. {s['name']} - API Key: {s['api_key']}")
        elif choice == '3':
            sid = int(input("Enter External Server ID: "))
            new_key = input("Enter the updated API key: ")
            if external_controller.update_api_key(sid, new_key):
                print("✅ API key updated successfully.")
            else:
                print("❌ Failed to update API key.")
        elif choice == '4':
            name = input("Enter new category name: ").lower()
            from server.controllers.category_controller import CategoryController
            cc = CategoryController()
            if cc.add_category(name):
                print("✅ Category added.")
            else:
                print("❌ Failed to add category.")
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid option. Try again.")



def show_user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. View Today's News")
        print("2. View News by Date Range")
        print("3. View News by Category & Date")
        print("4. Saved Articles")
        print("5. Notifications")
        print("6. Logout")

        choice = input("Choose: ")

        if choice == '1':
            response = api.request("GET", "/news/today")
            show_saved_menu.print_articles(response)
        elif choice == '2':
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            response = api.request("POST", "/news/range", {"start_date": start, "end_date": end})
            show_saved_menu.print_articles(response)
        elif choice == '3':
            cat = input("Category (business/entertainment/sports/technology): ")
            date = input("Date (YYYY-MM-DD): ")
            response = api.request("POST", "/news/by-category", {"category": cat, "date": date})
            show_saved_menu.print_articles(response)
        elif choice == '4':
            show_saved_menu()
        elif choice == '5':
            show_notification_menu()
        elif choice == '6':
            session.logout()
            print("Logged out.")
            break
        else:
            print("Invalid choice.")



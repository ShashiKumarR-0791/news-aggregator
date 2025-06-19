from datetime import datetime
from client.services.api_client import APIClient
from client.services.session_manager import SessionManager
from client.ui.headline_ui import show_headlines_menu
from client.ui.search_ui import show_search_menu
from client.ui.notification_ui import show_notification_menu
from server.controllers.category_controller import CategoryController
from server.controllers.external_server_controller import ExternalServerController
from client.ui.saved_ui import show_saved_menu

api = APIClient()
session = SessionManager()
external_controller = ExternalServerController()
cc = CategoryController()

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
        # ✅ Fix: Properly store user and token in session
        session.login(user=response["user"], token=response.get("token"))
        print(f"Welcome {response['user'].get('username', 'User')}!")
        show_dashboard()
    else:
        print("❌", response.get("message") or response.get("error"))

def signup():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    # Always assign role as 'user'
    response = api.request("POST", "/signup", {
        "username": username,
        "email": email,
        "password": password,
        "role": "user"
    })

    print("✅ Signup successful!" if response.get("success") else f"❌ {response.get('message') or response.get('error')}")

def show_dashboard():
    if session.get_role() == 'admin':
        show_admin_menu()
    else:
        show_user_menu()

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
                dict_s = dict(s)
                status = "Active" if dict_s.get("is_active") else "Not Active"
                print(f"{dict_s.get('server_id', dict_s.get('id'))}. {dict_s.get('name')} - {status} - Last Accessed: {dict_s.get('last_accessed') or 'N/A'}")

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
            name = input("Enter new category name: ").strip().lower()
            if cc.add_category(name):
                print(f"✅ Category '{name}' added.")
            else:
                print("❌ Failed to add category.")
        elif choice == '5':
            print("Logged out.")
            session.logout()
            break
        else:
            print("Invalid option. Try again.")

def show_user_menu():
    user = session.get_user()
    if not user:
        print("❌ Invalid user session. Please log in again.")
        return

    while True:
        today = datetime.now().strftime('%d-%b-%Y')
        time = datetime.now().strftime('%I:%M%p')

        print(f"\nWelcome to the News Application, {user.get('username', 'User')}! Date: {today} Time: {time}")
        print("Please choose the options below")
        print("1. Headlines")
        print("2. Saved Articles")
        print("3. Search")
        print("4. Notifications")
        print("5. Logout")

        choice = input("Choose: ").strip()
        if choice == '1':
            show_headlines_menu(user)
        elif choice == '2':
            show_saved_menu()
        elif choice == '3':
            show_search_menu(user)
        elif choice == '4':
            show_notification_menu(user)
        elif choice == '5':
            session.logout()
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Try again.")

from datetime import datetime
from client.services.api_client import APIClient
from client.services.session_manager import SessionManager
from client.ui.headline_ui import show_headlines_menu
from client.ui.search_ui import show_search_menu
from client.ui.notification_ui import show_notification_menu
from client.utils.report_article import view_reported_articles
from client.utils.show_saved_menu import show_saved_menu
from client.api.news_api import get_most_liked_articles, get_reported_articles, delete_article
from client.ui.article_ui import display_articles
from client.api.news_api import interact_with_articles
from server.controllers.category_controller import CategoryController
from server.controllers.external_server_controller import ExternalServerController

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
        session.login(user=response["user"], token=response.get("token"))
        print(f"Welcome {response['user'].get('username', 'User')}!")
        show_dashboard()
    else:
        print("", response.get("message") or response.get("error"))

def signup():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    response = api.request("POST", "/signup", {
        "username": username,
        "email": email,
        "password": password,
        "role": "user"
    })

    print(" Signup successful!" if response.get("success") else f" {response.get('message') or response.get('error')}")

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
        print("5. Manage Reported Articles")
        print("6. View Hidden Articles")
        print("7. Logout")
        
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
                print(" API key updated successfully.")
            else:
                print(" Failed to update API key.")
        elif choice == '4':
            name = input("Enter new category name: ").strip().lower()
            if cc.add_category(name):
                print(f" Category '{name}' added.")
            else:
                print(" Failed to add category.")
        elif choice == '5':
            manage_reported_articles()
        elif choice == '6':
            view_hidden_articles()
        elif choice == '7':
            print("Logged out.")
            session.logout()
            break
        else:
            print("Invalid option. Try again.")

def show_user_menu():
    user = session.get_user()
    if not user:
        print(" Invalid user session. Please log in again.")
        return

    while True:
        today = datetime.now().strftime('%d-%b-%Y')
        time = datetime.now().strftime('%I:%M%p')

        print(f"\nWelcome to the News Application, {user.get('username', 'User')}! Date: {today} Time: {time}")
        print("Please choose the options below")
        print("1. Headlines")
        print("2. Saved Articles")
        print("3. Search")
        print("4. Most Liked Articles")
        print("5. Logout")

        choice = input("Choose: ").strip()
        if choice == '1':
            show_headlines_menu(user)
        elif choice == '2':
            show_saved_menu()
        elif choice == '3':
            show_search_menu(user)
        elif choice == '4':
            show_most_liked_articles(user)
        elif choice == '5':
            session.logout()
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Try again.")

def show_most_liked_articles(user):
    print("\n--- Most Liked Articles ---")
    print("Fetching articles with the most likes...")
    
    response = get_most_liked_articles()
    if isinstance(response, dict):
        articles = response.get("articles", [])
    elif isinstance(response, list):
        articles = response
    else:
        articles = []
    
    if articles:
        print(f"Found {len(articles)} most liked articles:")
        display_articles(articles)
        interact_with_articles(articles, user)
    else:
        print("No liked articles found.")

def manage_reported_articles():
    print("\n--- Manage Reported Articles ---")
    print("Fetching all reported articles...")
    
    response = get_reported_articles()
    print("DEBUG: Raw response from server:", response)  
    if isinstance(response, dict):
        articles = response.get("articles", [])
    elif isinstance(response, list):
        articles = response
    else:
        articles = []
    
    print("DEBUG: Parsed articles:", articles) 
    if not articles:
        print("No reported articles found.")
        return
    
    print(f"\nFound {len(articles)} reported articles:")
    
    for i, article in enumerate(articles, 1):
        if not isinstance(article, dict):
            print(f"\n{i}. [Invalid article data: {article}]")
            continue
        print(f"\n{i}. {article.get('title', 'No Title')}")
        print(f"   Source: {article.get('source', 'Unknown')}")
        print(f"   Published: {article.get('published_at', 'Unknown')}")
        print(f"   Report Count: {article.get('report_count', 0)}")
        print(f"   Status: {'Hidden' if article.get('is_hidden') else 'Visible'}")
        print(f"   Article ID: {article.get('article_id')}")
    
    while True:
        print("\nOptions:")
        print("1. Delete an article")
        print("2. Back to admin menu")
        
        choice = input("Choose: ").strip()
        
        if choice == '1':
            try:
                article_id = int(input("Enter Article ID to delete: "))
                confirm = input(f"Are you sure you want to delete article {article_id}? (yes/no): ").strip().lower()
                
                if confirm == 'yes':
                    result = delete_article(article_id)
                    if isinstance(result, dict):
                        print(f" {result.get('message', result.get('error', 'No message'))}")
                        return manage_reported_articles()
                    else:
                        print(f" Error: Unexpected response: {result}")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid Article ID.")
        elif choice == '2':
            break
        else:
            print("Invalid choice.")

def view_hidden_articles():
    print("\n--- Hidden Articles (is_hidden=1) ---")
    import requests
    from client.session import session
    BASE_URL = "http://localhost:8000"
    try:
        response = requests.get(f"{BASE_URL}/admin/hidden-articles", headers=session.get_headers())
        data = response.json()
    except Exception as e:
        print(f" Failed to fetch hidden articles: {e}")
        return
    articles = data.get("articles") if isinstance(data, dict) else data
    if not articles:
        print(" No hidden articles found.")
        return
    print(f"\nFound {len(articles)} hidden articles:")
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article.get('title', 'No Title')}")
        print(f"   Source: {article.get('source', 'Unknown')}")
        print(f"   Published: {article.get('published_at', 'Unknown')}")
        print(f"   Likes: {article.get('likes', 0)} | Dislikes: {article.get('dislikes', 0)}")
        print(f"   Article ID: {article.get('article_id')}")
    while True:
        print("\nOptions:")
        print("1. Delete an article")
        print("2. Back to admin menu")
        choice = input("Choose: ").strip()
        if choice == '1':
            try:
                article_id = int(input("Enter Article ID to delete: "))
                confirm = input(f"Are you sure you want to delete article {article_id}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    from client.api.news_api import delete_article
                    result = delete_article(article_id)
                    if isinstance(result, dict):
                        print(f" {result.get('message', result.get('error', 'No message'))}")
                        return view_hidden_articles()
                    else:
                        print(f" Error: Unexpected response: {result}")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid Article ID.")
        elif choice == '2':
            break
        else:
            print("Invalid choice.")

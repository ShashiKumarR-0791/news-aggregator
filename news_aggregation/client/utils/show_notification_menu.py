from client.services.api_client import APIClient
from client.services.session_manager import SessionManager

api = APIClient()
session = SessionManager()
def show_notification_menu():
    while True:
        print("\n--- Notifications ---")
        print("1. View")
        print("2. Configure")
        print("3. View Configs")
        print("4. Back")
        choice = input("Choose: ")
        if choice == '1':
            res = api.request("POST", "/notifications/view", {"user_id": session.get_user_id()})
            for n in res:
                print(f"[{n['type']}] {n['message']} | Read: {n['is_read']}")
        elif choice == '2':
            cat = input("Category (e.g., business/sports/keywords): ")
            enabled = input("Enable? (y/n): ").lower() == 'y'
            kw = input("Keywords (comma-separated): ") if cat.lower() == "keywords" else ""
            res = api.request("POST", "/notifications/configure", {
                "user_id": session.get_user_id(),
                "category": cat,
                "is_enabled": enabled,
                "keywords": kw
            })
            print(res.get("message") or res.get("error"))
        elif choice == '3':
            res = api.request("POST", "/notifications/configs", {"user_id": session.get_user_id()})
            for c in res:
                print(f"{c['category']} - {'Enabled' if c['is_enabled'] else 'Disabled'} - Keywords: {c.get('keywords')}")
        elif choice == '4':
            break

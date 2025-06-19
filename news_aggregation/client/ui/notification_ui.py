from client.api import notification_api
from client.session import session

def show_notification_menu(user):
    while True:
        print("\n--- 🔔 Notification Menu ---")
        print("1. View My Notifications")
        print("2. Configure Category Notifications")
        print("3. Update Keyword Alerts")
        print("4. Back")

        choice = input("Choose: ").strip()

        if choice == '1':
            try:
                notifications = notification_api.get_notifications()
                if not notifications:
                    print("❌ No notifications found.")
                else:
                    print("\n📨 Your Notifications:")
                    for n in notifications:
                        status = "🔔 New" if not n.get("is_read") else "✔️ Read"
                        print(f"\n[{status}] {n['created_at']}")
                        print(f"📩 {n['message']}")
            except Exception as e:
                print(f"❌ Failed to load notifications: {e}")

        elif choice == '2':
            try:
                configs = notification_api.get_config()
                if not configs:
                    print("ℹ️ No notification preferences found.")
                else:
                    print("\n🔧 Your Category Notification Preferences:")
                    for c in configs:
                        status = "✅ Enabled" if c['is_enabled'] else "❌ Disabled"
                        print(f"{c['category'].capitalize()}: {status} | Keywords: {c.get('keywords', 'None')}")

                category = input("Enter category to update: ").strip().lower()
                is_enabled = input("Enable this category? (yes/no): ").strip().lower() == "yes"
                success = notification_api.update_config(category, is_enabled)
                print("✅ Category updated successfully." if success else "❌ Failed to update category.")
            except Exception as e:
                print(f"❌ Error updating category: {e}")

        elif choice == '3':
            keywords = input("Enter comma-separated keywords (e.g. ai,crypto,election): ").strip()
            success = notification_api.update_keywords(keywords)
            print("✅ Keywords updated." if success else "❌ Failed to update keywords.")

        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

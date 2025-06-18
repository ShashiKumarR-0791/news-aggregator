import sqlite3,os

def show_categories():
    try:
        

        db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()



        cursor.execute("SELECT category_id, name, description, is_active, created_at FROM categories")
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ No categories found.")
            return

        print("\n📂 Categories in Database:\n")
        for row in rows:
            category_id, name, desc, is_active, created_at = row
            print(f"🆔 ID: {category_id} | 🏷️ Name: {name} | 📃 Description: {desc or 'N/A'} | ✅ Active: {bool(is_active)} | 📅 Created: {created_at}")

        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_categories()

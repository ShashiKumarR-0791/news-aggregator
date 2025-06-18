import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'news_aggregator.db')
 

def get_category_id(cursor, category_name):
    query = "SELECT category_id FROM categories WHERE LOWER(name) = LOWER(?)"
    cursor.execute(query, (category_name,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_articles_by_category(category_name):
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    category_id = get_category_id(cursor, category_name)
    if not category_id:
        print(f"❌ Category '{category_name}' not found in DB.")
        conn.close()
        return

    print(f"\n📚 Articles in category '{category_name}' (ID: {category_id}):\n")

    query = """
        SELECT title, source, published_at, url
        FROM news_articles
        WHERE category_id = ?
        ORDER BY published_at DESC
        LIMIT 10
    """
    cursor.execute(query, (category_id,))
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No articles found in this category.")
    else:
        for row in rows:
            print(f"📰 {row['title']}")
            print(f"   Source: {row['source']}")
            print(f"   Published At: {row['published_at']}")
            print(f"   URL: {row['url']}\n")

    conn.close()

if __name__ == "__main__":
    category = input("Enter category name (e.g. business, sports): ").strip()
    get_articles_by_category(category)

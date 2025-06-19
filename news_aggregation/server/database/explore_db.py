import sqlite3
import os
from datetime import datetime, timezone

# DB connection
db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tables
print(" Tables in the database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
for t in tables:
    print(" -", t)

# Users
if "users" in tables:
    print("\n👤 Users:")
    cursor.execute("SELECT user_id, username, email, role FROM users;")
    for row in cursor.fetchall():
        print(row)

# External Servers
if "external_servers" in tables:
    print("\n External Servers:")
    cursor.execute("SELECT server_id, name, api_url, api_key, is_active FROM external_servers;")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Active: {bool(row[4])}, URL: {row[2]}")

# News Articles (Last 5)
if "news_articles" in tables:
    print("\n Recent News Articles:")
    cursor.execute("SELECT article_id, title, published_at, source FROM news_articles ORDER BY published_at DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1][:60]} ({row[2]}) from {row[3]}")

# Today's Articles
if "news_articles" in tables:
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    print(f"\n📅 Articles Published Today ({today}):")
    cursor.execute("SELECT article_id, title, published_at FROM news_articles WHERE DATE(published_at) = DATE(?)", (today,))
    today_articles = cursor.fetchall()
    if today_articles:
        for a in today_articles:
            print(f"{a[0]}: {a[1][:60]} ({a[2]})")
    else:
        print("No articles found for today.")

conn.close()

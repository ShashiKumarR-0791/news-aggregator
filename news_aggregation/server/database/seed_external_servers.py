import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

external_servers = [
    (
        "NewsAPI",
        "https://newsapi.org/v2/top-headlines?country=us&category=business",
        "af3ce09176fb4fd3be6fcfd1e000776c"
    ),
    (
        "TheNewsAPI",
        "https://api.thenewsapi.com/v1/news/top?locale=us&limit=3",
        "af3ce09176fb4fd3be6fcfd1e000776c"
    ),
    (
        "Firebase",
        "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi?country=us&category=business",
        "af3ce09176fb4fd3be6fcfd1e000776c"
    )
]


for name, api_url, api_key in external_servers:
    cursor.execute('''
        INSERT OR IGNORE INTO external_servers (name, api_url, api_key, is_active, created_at)
        VALUES (?, ?, ?, 1, datetime('now'))
    ''', (name, api_url, api_key))

conn.commit()
conn.close()

print(" External servers seeded successfully.")

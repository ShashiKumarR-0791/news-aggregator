import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ✅ Use your actual API key here
REAL_KEY = "af3ce09176fb4fd3be6fcfd1e000776c"
The_API_KEY="E59Lzz4zfUYOtWZ3zQGV8Ofo9Vj7RcSNX02LcSet"

# Update NewsAPI
cursor.execute("""
    UPDATE external_servers
    SET api_url = 'https://newsapi.org/v2/top-headlines?country=us&category=business',
        api_key = ?
    WHERE name = 'NewsAPI'
""", (REAL_KEY,))

# Update TheNewsAPI
cursor.execute("""
    UPDATE external_servers
    SET api_url = 'https://api.thenewsapi.com/v1/news/top',
        api_key = ?
    WHERE name = 'TheNewsAPI'
""", (The_API_KEY,))

# Fix Firebase (no API key needed)
cursor.execute("""
    UPDATE external_servers
    SET api_url = 'https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi?country=us&category=business',
        api_key = ''
    WHERE name = 'Firebase'
""")

conn.commit()
conn.close()
print("✅ External server URLs and API keys have been fixed.")

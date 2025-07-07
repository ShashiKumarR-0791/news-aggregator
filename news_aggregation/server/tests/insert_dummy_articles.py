
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Titles of dummy articles
dummy_titles = [
    "AI Breakthrough",
    "Elections 2025",
    "Tech Giants Merge",
    "Sports: Finals Today",
    "Economy Watch"
]

# Delete articles with matching titles
for title in dummy_titles:
    cursor.execute("DELETE FROM news_articles WHERE title = ?", (title,))
    print(f"🗑️ Deleted: {title}")

conn.commit()
conn.close()

print(" All dummy articles deleted.")

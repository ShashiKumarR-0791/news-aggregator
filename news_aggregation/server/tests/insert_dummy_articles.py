# import sqlite3
# import os
# from datetime import datetime, timezone

# db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# now = datetime.now(timezone.utc).isoformat()

# dummy_articles = [
#     ("AI Breakthrough", "OpenAI achieves GPT-5 milestone.", "Full content here.", "https://news.com/ai", "OpenAI", 1, now),
#     ("Elections 2025", "National elections in full swing.", "Details inside.", "https://news.com/election", "CNN", 2, now),
#     ("Tech Giants Merge", "Big merger shocks industry.", "Merged companies listed.", "https://news.com/merge", "TechCrunch", 3, now),
#     ("Sports: Finals Today", "Championship games underway.", "Match details here.", "https://news.com/sports", "ESPN", 4, now),
#     ("Economy Watch", "Markets show mixed results.", "Stock trends analyzed.", "https://news.com/market", "Reuters", 1, now),
# ]

# for title, desc, content, url, source, category_id, pub_date in dummy_articles:
#     cursor.execute("""
#         INSERT OR IGNORE INTO news_articles
#         (title, description, content, url, source, category_id, published_at, created_at, likes, dislikes)
#         VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), 0, 0)
#     """, (title, desc, content, url, source, category_id, pub_date))

# conn.commit()
# conn.close()

# print(" Inserted 5 dummy news articles for today.")
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

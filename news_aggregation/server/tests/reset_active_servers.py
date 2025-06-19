# import sqlite3
# import os

# db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Activate only Firebase
# cursor.execute("UPDATE external_servers SET is_active = 1 WHERE name = 'Firebase'")
# cursor.execute("UPDATE external_servers SET is_active = 0 WHERE name != 'Firebase'")

# conn.commit()
# conn.close()

# print(" Only Firebase server is active now.")
# server/database/enable_newsapi_only.py
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'news_aggregator.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("UPDATE external_servers SET is_active = 1 WHERE name = 'NewsAPI'")
cursor.execute("UPDATE external_servers SET is_active = 0 WHERE name != 'NewsAPI'")

conn.commit()
conn.close()
print(" Only NewsAPI is now active.")

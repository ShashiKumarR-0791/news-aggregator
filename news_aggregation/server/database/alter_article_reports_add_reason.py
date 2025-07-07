import sqlite3

DB_PATH = 'server/database/news_aggregator.db'

ALTER_SQL = "ALTER TABLE article_reports ADD COLUMN reason TEXT;"

# Check if the column already exists
def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not column_exists(cur, 'article_reports', 'reason'):
        try:
            cur.execute(ALTER_SQL)
            conn.commit()
            print("Column 'reason' added to article_reports table.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Column 'reason' already exists.")
    conn.close()

if __name__ == "__main__":
    main() 
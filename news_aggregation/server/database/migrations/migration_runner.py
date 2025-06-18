import sqlite3
import os

SQL_PATH = os.path.join(os.path.dirname(__file__), '001_initial_schema.sql')
DB_PATH = os.path.join(os.path.dirname(__file__), '../news_aggregator.db')

def run_migration():
    with open(SQL_PATH, 'r') as file:
        sql_script = file.read()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✅ Database schema created successfully.")

if __name__ == "__main__":
    run_migration()

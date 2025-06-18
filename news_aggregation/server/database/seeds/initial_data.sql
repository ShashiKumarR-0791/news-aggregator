import os
import psycopg2
from server.config.database import DatabaseConfig
import logging

logger = logging.getLogger(__name__)

class MigrationRunner:
    """Database migration runner"""
    
    def __init__(self):
        self.config = DatabaseConfig.get_config()
    
    def run_migrations(self):
        """Run all pending migrations"""
        try:
            connection = psycopg2.connect(**self.config)
            cursor = connection.cursor()
            
            # Create migrations table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL UNIQUE,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Get migrations directory
            migrations_dir = os.path.dirname(__file__)
            
            # Get all SQL files
            sql_files = [f for f in os.listdir(migrations_dir) if f.endswith('.sql')]
            sql_files.sort()
            
            for sql_file in sql_files:
                # Check if migration already executed
                cursor.execute("SELECT id FROM migrations WHERE filename = %s", (sql_file,))
                if cursor.fetchone():
                    continue
                
                # Execute migration
                with open(os.path.join(migrations_dir, sql_file), 'r') as f:
                    sql_content = f.read()
                
                cursor.execute(sql_content)
                
                # Record migration
                cursor.execute(
                    "INSERT INTO migrations (filename) VALUES (%s)",
                    (sql_file,)
                )
                
                logger.info(f"Executed migration: {sql_file}")
            
            connection.commit()
            logger.info("All migrations completed successfully")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


if __name__ == "__main__":
    # Run migrations
    runner = MigrationRunner()
    runner.run_migrations()
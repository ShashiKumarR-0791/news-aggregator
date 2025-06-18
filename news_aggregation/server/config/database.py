from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConfig:
    """Database configuration settings"""
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Get database connection string"""
        return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    @classmethod
    def get_config(cls) -> dict:
        """Get database configuration as dictionary"""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'news_aggregation'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
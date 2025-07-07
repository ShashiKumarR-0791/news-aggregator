from datetime import datetime
from server.repositories.base_repository import BaseRepository
from server.models.category import Category

class CategoryRepository(BaseRepository):
    def add_category(self, category):
        try:
            name = category.name if hasattr(category, 'name') else str(category)
            query = "INSERT OR IGNORE INTO categories (name) VALUES (?)"
            self.execute(query, (name.lower(),))
            return True
        except Exception as e:
            print(f" Failed to add category: {e}")
            return False


    def get_all_categories(self):
        query = 'SELECT * FROM categories WHERE is_active = 1'
        rows = self.fetchall(query)
        return [dict(row) for row in rows]

    def get_category_id_by_name(self, name):
        try:
            if not isinstance(name, str):
                name = str(getattr(name, "name", name))
            query = "SELECT category_id FROM categories WHERE LOWER(name) = ?"
            result = self.fetchone(query, (name.lower(),))
            return result['category_id'] if result else None
        except Exception as e:
            print(f" Error in get_category_id_by_name: {e}")
            return None


from datetime import datetime
from server.repositories.base_repository import BaseRepository
from server.models.category import Category

class CategoryRepository(BaseRepository):
    def add_category(self, name: str, description: str = "", is_active: bool = True):
        if self.get_category_id_by_name(name):
            print(f"Category '{name}' already exists.")
            return

        category = Category(
            name=name,
            description=description,
            is_active=is_active,
            created_at=datetime.utcnow().isoformat()
        )

        query = '''
            INSERT INTO categories (name, description, is_active, created_at)
            VALUES (?, ?, ?, ?)
        '''
        self.execute(query, (
            category.name,
            category.description,
            int(category.is_active),
            category.created_at
        ))
        print(f" Category '{name}' added to DB.")

    def get_all_categories(self):
        query = 'SELECT * FROM categories WHERE is_active = 1'
        rows = self.fetchall(query)
        return [dict(row) for row in rows]

    def get_category_id_by_name(self, name):
        query = "SELECT category_id FROM categories WHERE LOWER(name) = ?"
        result = self.fetchone(query, (name.lower(),))
        return result['category_id'] if result else None

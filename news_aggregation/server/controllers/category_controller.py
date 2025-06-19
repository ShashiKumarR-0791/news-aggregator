from server.repositories.category_repository import CategoryRepository
from server.models.category import Category
from datetime import datetime

class CategoryController:
    def __init__(self):
        self.repo = CategoryRepository()

    def add_category(self, name: str, description: str = ""):
        try:
            category = Category(
                name=name,
                description=description,
                is_active=True,
                created_at=datetime.utcnow().isoformat()
            )
            self.repo.add_category(category)
            return True
        except Exception as e:
            print(f" Failed to add category: {e}")
            return False


    def list_categories(self):
        return self.repo.get_all_categories()

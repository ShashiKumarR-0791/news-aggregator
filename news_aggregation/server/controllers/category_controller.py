from server.repositories.category_repository import CategoryRepository

class CategoryController:
    def __init__(self):
        self.repo = CategoryRepository()

    def add_category(self, name):
        return self.repo.add_category(name)

    def list_categories(self):
        return self.repo.get_all_categories()


from category import Category
from operation import *
from storage import Storage

class FinanceManager:
    def __init__(self):
        Storage.ensure_structure()

    def add_operation(self, type, category, title, amount, date) -> Operation:
        id_set = Storage.get_op_id_set()
        if len(id_set) == 0:
            id = 1
        else:
            id = max(id_set) + 1

        op = Operation(id, type, category, title, amount, date)
        Storage.save_op(op)

        return op

    def edit_operation(self, old_op: Operation, new_op: dict) -> Operation | None:
        if old_op.id != new_op.get("id"):
            print("Ошибка сопоставления id... хуй знает как")
            return
        
        if new_op.get("type") != None:
            old_op.type = new_op.get("type")
        
        if new_op.get("category_id") != None:
            old_op.category_id = new_op.get("category_id")

        if new_op.get("title") != None:
            old_op.title = new_op.get("title")

        if new_op.get("amount") != None:
            old_op.amount = new_op.get("amount")

        if new_op.get("date") != None:
            old_op.date = new_op.get("date")

        return Storage.edit_op(old_op)

    def remove_operation(self, id: int):
        Storage.remove_op(id)

    def get_all_operations(self) -> list[Operation]:
        return Storage.load_all_op()
    
    def get_operation(self, id: int) -> Operation | None:
        return Storage.load_op(id)

    def operation_exists(self, id) -> bool:
        return self.get_operation(id) != None

    def filter_operations(self, period: str = None, category: str = None, type: str = None) -> list[Operation]:
        data = self.get_all_operations()
        filtered = []

        for op in data:
            if period and period not in op.date:
                continue
            
            if category and category.lower() != op.category.lower():
                continue
            
            if type and type.lower() != op.type.lower():
                continue

            filtered.append(op)

        return filtered
    
    def get_balance(self):
        pass

    def add_category(self, title) -> Category:
        id_set = Storage.get_cat_id_set()
        if len(id_set) == 0:
            id = 1
        else:
            id = max(id_set) + 1

        cat = Category(id, title)
        Storage.save_cat(cat)

        return cat

    def edit_category(self, id, title) -> Category | None:    
        return Storage.edit_cat(id, title)

    def remove_category(self, id: int):
        Storage.remove_cat(id)

    def get_all_categories(self) -> list[Category]:
        return Storage.load_all_cat()

    def get_category(self, id: int) -> Category | None:
        return Storage.load_cat(id)

    def get_category_by_title(self, title: str) -> Category | None:
        data = Storage.load_all_cat()
        for i in data:
            if i.title == title:
                return i
            
        return None

    def category_exists_by_title(self, title: str) -> bool:
        return self.get_category_by_title(title) != None

    def category_exists(self, id: int) -> bool:
        return self.get_category(id) != None
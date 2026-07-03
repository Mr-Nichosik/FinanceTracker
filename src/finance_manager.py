
from category import Category
from operation import *
from operation import Operation
from storage import Storage
from typing import Literal

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
        data: list[Operation] = self.get_all_operations()
        filtered = []

        for op in data:
            if period and period not in op.date:
                continue
            
            if category and category.lower() != op.category_id:
                continue
            
            if type and type.lower() != op.type.lower():
                continue

            filtered.append(op)

        return filtered
    
    def get_balance(self) -> dict:
        lst = dict()
        income = self.get_amount_by_op_type("доход")
        expenses = self.get_amount_by_op_type("расход")
        lst["income"] = income
        lst["expenses"] = expenses
        lst["balance"] = income-expenses
        return lst
    
    def get_amount_by_op_type(self, op_type: Literal["доход", "расход"]) -> float:
        amount = 0
        data = self.get_all_operations()
        for i in data:
            if i.type == op_type:
                amount += i.amount

        return amount     

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
    
    def category_linked(self, id: int) -> int:
        data = self.get_all_operations()
        lst = []

        for i in data:
            if i.category_id == id:
                lst.append(i)
        
        return len(lst)
    
    def get_amount_by_categories(self, op_type: Literal["доход", "расход"]) -> dict[int, float]:
        cats = self.get_all_categories()
        ops = self.get_all_operations()

        data = {cat.id: 0 for cat in cats}

        for op in ops:
            if op.type == op_type:
                data[op.category_id] += op.amount

        return data

if __name__ == "__main__":
    man = FinanceManager()
    print(man.get_amount_by_categories("доход"))
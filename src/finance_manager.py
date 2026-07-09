
from __future__ import annotations

from category import Category
from operation import Operation, OperationData, OPERATION_FIELDS, OperationType
from storage import Storage
from typing import TypedDict
from datetime import datetime
from enum import StrEnum

class Balance(TypedDict):
    income: float
    expenses: float
    balance: float

class SortType(StrEnum):
    DATE = "date"
    AMOUNT = "amount"
    CATEGORY = "category"

    @staticmethod
    def get_type(id: str | int) -> SortType | None:
        return {
            "1": SortType.DATE, 
            "2": SortType.AMOUNT,
            "3": SortType.CATEGORY,
            1: SortType.DATE, 
            2: SortType.AMOUNT,
            3: SortType.CATEGORY
        }.get(id)

class FinanceManager:
    def __init__(self):
        Storage.ensure_structure()

    def add_operation(self, data: OperationData) -> Operation:
        data["id"] = self.__create_id(Storage.get_op_id_set())
        
        op = Operation(**data)
        Storage.save_op(op)

        return op

    def edit_operation(self, old_op: Operation, new_data: OperationData) -> Operation | None:
        if old_op.id != new_data["id"]:
            print("FinanceManager log: edit_operation: id compression error")
            return
        
        for field in OPERATION_FIELDS:
            if new_data[field] is not None:
                setattr(old_op, field, new_data[field])

        return Storage.edit_op(old_op)

    def remove_operation(self, id: int):
        Storage.remove_op(id)

    def get_all_operations(self) -> list[Operation]:
        return Storage.load_all_op()
    
    def get_operation(self, id: int) -> Operation | None:
        return Storage.load_op(id)

    def operation_exists(self, id) -> bool:
        return self.get_operation(id) != None

    def get_operation_template(self) -> OperationData:
        return Operation.get_template()

    def filter_operations(self, period: str = None, category_title: str = None, type_id: str | int = None, sort_type: SortType = SortType.DATE) -> list[Operation]:
        data: list[Operation] = self.get_all_operations()
        filtered = []

        for op in data:
            if period and period not in op.date:
                continue
            
            if category_title and category_title != self.get_category(op.category_id).title:
                continue
            
            if type_id and OperationType.get_type(type_id) != op.type:
                continue

            filtered.append(op)

        if sort_type == SortType.DATE:
            return self.sort_by_date(filtered)
        elif sort_type == SortType.AMOUNT:
            return self.sort_by_amount(filtered)
        elif sort_type == SortType.CATEGORY:
            return self.sort_by_category(filtered)
    
    def get_balance(self) -> Balance:
        income = self.get_amount_by_op_type(OperationType.INCOME)
        expenses = self.get_amount_by_op_type(OperationType.EXPENSE)
        balance = income-expenses
        return Balance(income=income, expenses=expenses, balance=balance)
    
    def get_amount_by_op_type(self, op_type: OperationType) -> float:
        amount = 0
        data = self.get_all_operations()
        for i in data:
            if i.type == op_type:
                amount += i.amount

        return amount     

    def add_category(self, title) -> Category:
        cat = Category(self.__create_id(Storage.get_cat_id_set()), title)
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
        data = self.get_all_categories()
        for i in data:
            if i.title == title:
                return i
            
        return None

    def category_exists_by_title(self, title: str) -> bool:
        return self.get_category_by_title(title) != None

    def category_exists(self, id: int) -> bool:
        return self.get_category(id) != None
    
    def category_linked(self, id: int) -> int:
        """
        checks if category is linked with any operations.
        if it is not, returns 0
        """
        
        return len([op for op in self.get_all_operations() if op.id == id])  
    
    def get_amount_by_categories(self, op_type: OperationType) -> dict[int, float]:
        cats = self.get_all_categories()
        ops = self.get_all_operations()

        data = {cat.id: 0.0 for cat in cats}

        for op in ops:
            if op.type == op_type:
                data[op.category_id] += op.amount

        return data

    def sort_by_date(self, data: list[Operation]) -> list[Operation]:
        return sorted(data, key=lambda op: datetime.strptime(op.date, "%d.%m.%Y"))

    def sort_by_amount(self, data: list[Operation]) -> list[Operation]:
        return sorted(data, key=lambda op: op.amount)

    def sort_by_category(self, data: list[Operation]) -> list[Operation]:
        return sorted(data, key=lambda op: self.get_category(op.category_id).title)

    def get_n_operations(self, n: int) -> list[Operation]:
        data = self.sort_by_date(self.get_all_operations())

        return data[-n:]

    def __create_id(self, id_set: set) -> int:
        if len(id_set) == 0: return 1
        else: return max(id_set) + 1

if __name__ == "__main__":
    man = FinanceManager()
    print(man.get_amount_by_categories(OperationType.INCOME))
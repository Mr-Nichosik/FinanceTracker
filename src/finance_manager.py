
from operation import *
from storage import *

class FinanceManager:
    def __init__(self):
        pass

    def get_id_set(self) -> set:
        pass

    def add_operation(self, type, category, title, amount, date):
        # add id generator!
        id = 0

        op = Operation(id, type, category, title, amount, date)
        Storage.save(op)

    def get_all_operations(self) -> list[Operation]:
        return Storage.load_all()
    
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
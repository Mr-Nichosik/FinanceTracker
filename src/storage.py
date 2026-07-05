
from category import Category
from operation import *
import os
import shutil
import json

from operation import Operation, OperationData, OPERATION_FIELDS

class Storage:
    __currentFolder = os.path.dirname(os.path.abspath(__file__))
    __fileName = os.path.join(__currentFolder, "data.json")

    __operationSectionTitle = "Tasks"
    __categorySectionTitle = "Categories"
    __defaultObject: dict[str, list] = {__operationSectionTitle: [], __categorySectionTitle: []}

    @staticmethod
    def load_all_op() -> list[Operation]:
        return [Operation.from_dict(op) for op in Storage.__raw_load().get(Storage.__operationSectionTitle, [])]

    @staticmethod
    def load_op(id: int) -> Operation | None:
        data: list[OperationData] = Storage.__raw_load().get(Storage.__operationSectionTitle, [])
        for i in data:
            if i["id"] == id:
                return Operation.from_dict(i)
        
        return None

    @staticmethod
    def save_op(operation: Operation):
        operation_dict = operation.to_dict()

        data = Storage.__raw_load()
        data.get(Storage.__operationSectionTitle).append(operation_dict)

        Storage.__save_data(data)

    @staticmethod
    def edit_op(new_op_data: Operation) -> Operation | None:
        data = Storage.__raw_load()
        ops: list[OperationData] = [op for op in data.get(Storage.__operationSectionTitle, [])]

        for i in ops:
            if i["id"] == new_op_data.id:
                for field in OPERATION_FIELDS:
                    i[field] = getattr(new_op_data, field, i[field])

        Storage.__save_data(data)
        return Storage.load_op(new_op_data.id)

    @staticmethod
    def remove_op(id: int):
        data = Storage.__raw_load()
        new_data = [op for op in data.get(Storage.__operationSectionTitle, []) if op["id"] != id]
        data[Storage.__operationSectionTitle] = new_data
        Storage.__save_data(data)

    @staticmethod
    def get_op_id_set() -> set[int]:
        data: list[Operation] = Storage.load_all_op()
        id_set = set()
        for i in data:
            id_set.add(i.id)
        return id_set

    @staticmethod
    def load_all_cat() -> list[Category]:
        cat_list = []

        data = Storage.__raw_load()
        for i in data.get(Storage.__categorySectionTitle, []):
            i: Category = Category.from_dict(i)
            cat_list.append(i)

        return cat_list

    @staticmethod
    def load_cat(id: int) -> Category | None:
        data = Storage.__raw_load()
        for i in data.get(Storage.__categorySectionTitle, []):
            if i.get("id") == id:
                return Category.from_dict(i)
        
        return None

    @staticmethod
    def save_cat(cat: Category):
        cat_dict = cat.to_dict()

        data = Storage.__raw_load()
        data.get(Storage.__categorySectionTitle).append(cat_dict)

        Storage.__save_data(data)

    @staticmethod
    def edit_cat(id: int, title) -> Category | None:
        data = Storage.__raw_load()
        for i in data.get(Storage.__categorySectionTitle, []):
            if i.get("id") == id:
                i["title"] = title

        Storage.__save_data(data)
        return Storage.load_cat(id)

    @staticmethod
    def remove_cat(id: int):
        data = Storage.__raw_load()
        new_categories = [cat for cat in data.get(Storage.__categorySectionTitle, []) if cat.get("id") != id]
        data[Storage.__categorySectionTitle] = new_categories
        Storage.__save_data(data)

    @staticmethod
    def get_cat_id_set() -> set[int]:
        data: list[Category] = Storage.load_all_cat()
        id_set = set()
        for i in data:
            id_set.add(i.id)
        return id_set

    @staticmethod
    def __raw_load() -> dict[str, list]:
        Storage.ensure_structure()

        with open(Storage.__fileName, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def __save_data(data: dict):
        with open(Storage.__fileName, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def __create_file():
        with open(Storage.__fileName, "w", encoding="utf-8") as file:
            json.dump(Storage.__defaultObject, file, ensure_ascii=False, indent=4)

    @staticmethod
    def __check_file():
        if os.path.exists(Storage.__fileName) == False:
            Storage.__create_file()
        
    @staticmethod
    def __creat_backup():
        shutil.copy(Storage.__fileName, os.path.join(Storage.__currentFolder, "data.backup.json"))

    @staticmethod
    def ensure_structure():
        Storage.__check_file()

        try:
            with open(Storage.__fileName, "r", encoding="utf-8") as file:
                data: dict[str, list] = json.load(file)

            if Storage.__operationSectionTitle in data and Storage.__categorySectionTitle in data: return

            Storage.__creat_backup()

            if Storage.__operationSectionTitle not in data and Storage.__categorySectionTitle not in data:  
                Storage.__create_file()

            elif Storage.__operationSectionTitle in data and Storage.__categorySectionTitle not in data:
                data[Storage.__categorySectionTitle] = []
            elif Storage.__operationSectionTitle not in data and Storage.__categorySectionTitle in data:
                data[Storage.__operationSectionTitle] = []

            with open(Storage.__fileName, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except json.JSONDecodeError:
            Storage.__creat_backup()
            Storage.__create_file()

    @staticmethod
    def get_category_amount(cat_id: int) -> float:
        data = Storage.load_all_op()
        amount = 0
        for i in data:
            if i.category_id == cat_id:
                amount += i.amount

        return amount

if __name__ == "__main__":
    pass
        
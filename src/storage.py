
from category import Category
from operation import *
import os
import shutil
import json

from operation import Operation

class Storage:
    __currentFolder = os.path.dirname(os.path.abspath(__file__))
    __fileName = os.path.join(__currentFolder, "data.json")

    __operationSectionTitle = "Tasks"
    __categorySectionTitle = "Categories"
    __defaultObject: dict[str, list] = {__operationSectionTitle: [], __categorySectionTitle: []}

    @staticmethod
    def load_all_op() -> list[Operation]:
        op_list = []

        data = Storage.__raw_load()
        for i in data.get(Storage.__operationSectionTitle, []):
            i: Operation = Operation.from_dict(i)
            op_list.append(i)

        return op_list

    @staticmethod
    def load_op(id: int) -> Operation | None:
        data = Storage.__raw_load()
        for i in data.get(Storage.__operationSectionTitle, []):
            if i.get("id") == id:
                return Operation.from_dict(i)
        
        return None

    @staticmethod
    def save_op(operation: Operation):
        operation_dict = operation.to_dict()

        data = Storage.__raw_load()
        data.get(Storage.__operationSectionTitle).append(operation_dict)

        Storage.__save_data(data)

    @staticmethod
    def edit_op(new_op_data: Operation) -> Operation:
        data = Storage.__raw_load()
        for i in data.get(Storage.__operationSectionTitle, []):
            if i.get("id") == new_op_data.id:
                i["type"] = new_op_data.type
                i["category_id"] = new_op_data.category_id
                i["title"] = new_op_data.title
                i["amount"] = new_op_data.amount
                i["date"] = new_op_data.date

        Storage.__save_data(data)
        return Storage.load_op(new_op_data.id)

    @staticmethod
    def remove_op(id: int):
        pass

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
    def edit_cat(id: int, title) -> Category:
        data = Storage.__raw_load()
        for i in data.get(Storage.__categorySectionTitle, []):
            if i.get("id") == id:
                i["title"] = title

        Storage.__save_data(data)
        return Storage.load_cat(id)

    @staticmethod
    def get_cat_id_set() -> set[int]:
        data: list[Category] = Storage.load_all_cat()
        id_set = set()
        for i in data:
            id_set.add(i.id)
        return id_set

    @staticmethod
    def __raw_load() -> dict[str, list[dict]]:
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
            with open(Storage.__fileName, "r") as file:
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

if __name__ == "__main__":
    print(Storage.load_all_cat())
        
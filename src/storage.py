
from category import Category
from operation import *
import os
import shutil
import json

from operation import Operation

class Storage:
    __currentFolder = os.path.dirname(os.path.abspath(__file__))
    __fileName = os.path.join(__currentFolder, "data.json")
    __defaultObject: dict[str, list] = {"Tasks": [], "Categories": []}

    @staticmethod
    def load_all_op() -> list[Operation]:
        op_list = []

        data = Storage.__raw_load()
        for i in data.get("Tasks", []):
            i: Operation = Operation.from_dict(i)
            op_list.append(i)

        return op_list

    @staticmethod
    def load_op(id) -> Operation | None:
        Storage.ensure_structure()

        data = Storage.__raw_load()
        for i in data.get("Tasks", []):
            if i.get("id") == id:
                return Operation.from_dict(i)
        
        return None

    @staticmethod
    def save_op(operation: Operation):
        operation_dict = operation.to_dict()

        data = Storage.__raw_load()
        data.get("Tasks").append(operation_dict)

        Storage.__save_data(data)

    @staticmethod
    def edit_op(operation: Operation):
        pass

    @staticmethod
    def remove_op(id):
        pass

    @staticmethod
    def get_op_id_set() -> set[int]:
        data: list[Operation] = Storage.load_all_op()
        id_set = set()
        for i in data:
            id_set.add(i.id)
        return id_set

    @staticmethod
    def save_cat(cat: Category):
        cat_dict = cat.to_dict()

        data = Storage.__raw_load()
        data.get("Categories").append(cat_dict)

        Storage.__save_data(data)

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

            if "Tasks" in data and "Categories" in data: return

            Storage.__creat_backup()

            if "Tasks" not in data and "Categories" not in data:  
                Storage.__create_file()

            elif "Tasks" in data and "Categories" not in data:
                data["Categories"] = []
            elif "Tasks" not in data and "Categories" in data:
                data["Tasks"] = []

            with open(Storage.__fileName, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except json.JSONDecodeError:
            Storage.__creat_backup()
            Storage.__create_file()

if __name__ == "__main__":
    Storage.ensure_structure()
        
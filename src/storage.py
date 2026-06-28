
from operation import *
import os
import json

from operation import Operation

class Storage:
    __fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    __defaultObject = {"Tasks": []}

    @staticmethod
    def load_all() -> list[Operation]:
        op_list = []

        data = Storage.raw_load()
        for i in data.get("Tasks", []):
            i: Operation = Operation.from_dict(i)
            op_list.append(i)

        return op_list

    @staticmethod
    def load(id) -> Operation:
        Storage.__check_file()

    @staticmethod
    def raw_load() -> dict[str, list[dict]]:
        Storage.__check_file()

        with open(Storage.__fileName, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(operation: Operation):
        Storage.__check_file()

        operation_dict = operation.to_dict()

        data = Storage.raw_load()
        data.get("Tasks").append(operation_dict)

        with open(Storage.__fileName, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def remove(id):
        pass

    @staticmethod
    def get_id_set() -> set[int]:
        pass

    @staticmethod
    def __create_file():
        with open(Storage.__fileName, "w", encoding="utf-8") as file:
            json.dump(Storage.__defaultObject, file, ensure_ascii=False, indent=4)

    @staticmethod
    def __check_file():
        if os.path.exists(Storage.__fileName) == False:
            Storage.__create_file()
            return

        try:
            with open(Storage.__fileName, "r") as file:
                data = json.load(file)
            if "Tasks" not in data:
                Storage.__create_file()
        except json.JSONDecodeError:
            Storage.__create_file()
        
if __name__ == "__main__":
    Storage.save(Operation())
        
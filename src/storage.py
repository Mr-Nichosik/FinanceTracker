
from codecs import escape_encode
from operation import *
import os
import json

class Storage:
    __fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    __defaultObject = {"Tasks": []}

    @staticmethod
    def load(id):
        pass

    @staticmethod
    def load():
        Storage.__check_file()

        with open(Storage.__fileName, "r") as file:
            return json.load(file)

    @staticmethod
    def save(operation: Operation):
        pass

    @staticmethod
    def remove(id):
        pass

    @staticmethod
    def __create_file():
        with open(Storage.__fileName, "w") as file:
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
    print("use main.py")
        
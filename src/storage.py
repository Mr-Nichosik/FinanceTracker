
from codecs import escape_encode
from operation import *
import os
import json

class Storage:
    def __init__(self):
        self.__fileName = "data.json"
        self.__defaultObject = {"Tasks": []}

    def load(self, id):
        pass

    def save(self, operation: Operation):
        pass

    def remove(self, id):
        pass

    def __create_file(self):
        absPath = os.path.dirname(os.path.abspath(__file__))
        fileName = os.path.join(absPath, self.__fileName)
    
        with open(fileName, "w") as file:
            json.dump(self.__defaultObject, file, ensure_ascii=False, indent=4)

    def __check_file(self):
        absPath = os.path.dirname(os.path.abspath(__file__))
        fileName = os.path.join(absPath, self.__fileName)

        if os.path.exists(fileName) == False:
            self.__create_file()
            return

        try:
            with open(fileName, "r") as file:
                data = json.load(file)
            if "Tasks" not in data:
                self.__create_file()
        except json.JSONDecodeError:
            self.__create_file()
        
if __name__ == "__main__":
    storage = Storage()
    storage.load(1)
        
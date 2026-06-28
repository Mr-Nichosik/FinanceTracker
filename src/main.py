
import os
from operation import *
from storage import *

class Console:
    def __init__(self):
        self.__commands = [
            {"id": 0, "desc": "[DEBUG] Shows all tasks", "action": self.__show_all_operations},
            {"id": 1, "desc": "Показать данные за период", "action": self.show_operations_list},
            {"id": 2, "desc": "Добавить операцию", "action": self.show_operations_list},
        ]

        self.__errors = [
            {"id": 0, "desc": "<UnexpectedError>"},
            {"id": 1, "desc": "<CommandNotFoundError>"}
        ]

    # переработать систему ввода команд!!!
    def __input_command(self):
        # id = int(input("> "))
        # for i in self.__commands:
        #     if i.get("id") == id:
        #         return i["action"]
        # return 1   

        while True:
            try:
                command_id = int(input("> "))
                return command_id
            except Exception as e:
                print("Неверный формат ввода")

    def __show_menu(self):
        print("Доступные команды:")
        for i in self.__commands:
            if i.get("id") > 0:
                print(f"{i.get("id")}. {i.get("desc")}")

    def __show_error(self, id: int):
        for i in self.__errors:
            if i.get("id") == id:
                print(i.get("desc"))
                return

        # if the error id doesn't exist
        print(self.__errors[0].get("desc"))

    def __show_all_operations(self):
        data: dict = Storage.load()

        for i in data.get("Tasks", []):
            print(i)

    def run(self):
        while True:
            self.__show_menu()

            print()

            command_id = self.__input_command()
            os.system("cls")

            # if callable(function):
            #     function()
            # else:
            #     self.__show_error(function) # if it's not a funcm there will be an error id

            if any(item.get("id") == command_id for item in self.__commands):
                if command_id > 0:
                    next(item for item in self.__commands if item.get("id") == command_id).get("action")()
                else:
                    print("[DEBUG]")
                    next(item for item in self.__commands if item.get("id") == command_id).get("action")()

            else:
                self.__show_error(1)

            input()
            os.system("cls")

    def show_operations_list(self):
        print("Введите дату формата MM.YYYY или YYYY:")
        date = input(">")
        date = [x for x in date.split(".")]
        os.system("cls")

        # запрос к storage, cls обязательно

    def add_operation(self):
        op = Operation()

        print("Тип операции (доход/расход):")
        op.type = input(">")
        
        print("Категория:")
        op.category = input(">")
        
        print("Заголовок:")
        op.title = input(">")

        print("Дата:")
        op.date = input(">")

        # запрос к storage

if __name__ == "__main__":
    app = Console()
    app.run()
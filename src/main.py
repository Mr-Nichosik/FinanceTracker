
import os
from operation import Operation
from finance_manager import FinanceManager

class Console:
    def __init__(self):
        self.__commands = [
            {"id": 0, "desc": "[DEBUG] Shows all tasks", "prefix": "DEBUG", "action": self.__show_all_operations},
            {"id": 1, "desc": "Добавить операцию", "prefix": None, "action": self.add_operation},
            {"id": 2, "desc": "Фильтр", "prefix": None, "action": self.show_filtered_operations},
        ]

        self.__errors = [
            {"id": 0, "desc": "<UnexpectedError>"},
            {"id": 1, "desc": "<CommandNotFoundError>"}
        ]

        self.manager = FinanceManager()

    def __input_command(self): 
        while True:
            try:
                command_id = int(input("> "))
                return command_id
            except Exception as e:
                print("Неверный формат ввода")

    def __show_menu(self):
        print("Доступные команды:")
        for i in self.__commands:
            if not i.get("prefix"):
                print(f"{i.get("id")}. {i.get("desc")}")

    def __show_error(self, id: int):
        for i in self.__errors:
            if i.get("id") == id:
                print(i.get("desc"))
                return

        # if the error id doesn't exist
        print(self.__errors[0].get("desc"))

    def __show_operation(self, op: Operation):
        print(f"сумма: {op.amount} | тип: {op.type} | категория: {op.category} | дата: {op.date} | ID: {op.id} | описание: {op.title}")

    def __show_all_operations(self):
        data: list[Operation] = self.manager.get_all_operations()

        for i in data:
            self.__show_operation(i)

    def run(self):
        while True:
            self.__show_menu()

            print()

            command_id = self.__input_command()
            os.system("cls")

            command = next((item for item in self.__commands if item.get("id") == command_id), None)
            if command != None:
                if command.get("prefix"):
                    print(f"[{command.get("prefix")}]")
                    command.get("action")()
                else:
                    command.get("action")()
            else:
                self.__show_error(1)

            input()
            os.system("cls")

    def add_operation(self):
        while True:
            print("Тип операции (1 - расход | 2 - доход):")
            type = input("> ")
            if type == "1":
                type = "расход"
                break
            elif type == "2":
                type = "доход"
                break
            print("Неверный формат операции")

        print("Категория:")
        category = input("> ")
        
        print("Заголовок:")
        title = input("> ")

        while True:
            try:
                print("Сумма (формат дробных чисел - 100.5)")
                amount = float(input("> "))
                break
            except Exception as e:
                print("Неверный формат ввода")

        print("Дата:")
        date = input("> ")

        self.manager.add_operation(type, category, title, amount, date)

    def show_filtered_operations(self):
        print("Нажмите Enter, чтобы пропустить условие")
        print()

        print("Дата формата DD.MM.YYYY | MM.YYYY | YYYY:")
        date = input("> ")
        print()

        print("Категория:")
        category = input("> ")
        print()

        print("Тип:")
        type = input("> ")

        info = [date, category, type]
        for i in range(len(info)):
            if not info[i].strip():
                info[i] = None

        date, category, type = info

        data = self.manager.filter_operations(date, category, type)
        for i in data:
            self.__show_operation(i)
        

    # def show_operations_by_period(self):
    #     print("Введите дату формата DD.MM.YYYY, MM.YYYY или YYYY:")
    #     date = input("> ")
    #     os.system("cls")

    #     data = self.manager.get_operations_by_period(date)

    #     if not data:
    #         print("Данные не найдены")
    #         return

    #     print("Найденные операции:")
    #     for i in data:
    #         self.__show_operation(i)

    # def show_operations_by_category(self):
        # print("Укажите категорию: ")
        # category = input("> ")
        # os.system("cls")

        # data = self.manager.get_operations_by_category(category)

        # if not data:
        #     print("Данные не найдены")
        #     return

        # print("Найденные операции:")
        # for i in data:
        #     self.__show_operation(i)

if __name__ == "__main__":
    app = Console()
    app.run()
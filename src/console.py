
import os
from category import Category
from format import *
from operation import Operation
from finance_manager import FinanceManager


class Console:
    def __init__(self):
        self.__main_commands = [
            {
                "id": -1,
                "desc": "[DEBUG] Shows task by id",
                "prefix": "DEBUG",
                "action": self.__show_operation_by_id,
            },
            {
                "id": 0,
                "desc": "[DEBUG] Shows all tasks",
                "prefix": "DEBUG",
                "action": self.__show_all_operations,
            },
            {
                "id": 1,
                "desc": "Добавить операцию",
                "prefix": None,
                "action": self.add_operation,
            },
            {
                "id": 2,
                "desc": "Редактировать операцию",
                "prefix": None,
                "action": self.edit_operation,
            },
            {
                "id": 3,
                "desc": "Удалить операцию",
                "prefix": None,
                "action": self.remove_operation,
            },
            {
                "id": 4,
                "desc": "Фильтр",
                "prefix": None,
                "action": self.show_filtered_operations,
            },
            {
                "id": 5,
                "desc": "Управление категориями",
                "prefix": None,
                "action": self.categories_control,
            },
        ]

        self.__category_commands = [
            {"id": 1, "desc": "Создать", "prefix": None, "action": self.add_category},
            {
                "id": 2,
                "desc": "Редактировать",
                "prefix": None,
                "action": self.edit_category,
            },
            {
                "id": 3,
                "desc": "Удалить",
                "prefix": None,
                "action": self.remove_category,
            },
        ]

        self.__errors = [
            {"id": 0, "desc": "<UnexpectedError>"},
            {"id": 1, "desc": "<CommandNotFoundError>"},
        ]

        self.manager = FinanceManager()

    def __prompt(self) -> str:
        data = input(f"{CYAN}>{RESET} {UNDERLINE}")
        print(f"{RESET}")
        return data

    def __input_command(self):
        while True:
            try:
                command_id = int(self.__prompt())
                return command_id
            except Exception as e:
                print("Неверный формат ввода")

    def __run_menu(self, commands: list[dict], showWithPrefix=False, clearScreen=False):
        print("Доступные действия:")

        for i in commands:
            if showWithPrefix == True and i.get("prefix"):
                print(f"{i.get("id")}. {i.get("desc")}")

            if not i.get("prefix"):
                print(f"{i.get("id")}. {i.get("desc")}")

        command_id = self.__input_command()
        if clearScreen:
            os.system("cls")

        command = next(
            (item for item in commands if item.get("id") == command_id), None
        )
        if command != None:
            if command.get("prefix"):
                print(f"[{command.get("prefix")}]")
            command.get("action")()
        else:
            self.__show_error(1)

    def __show_error(self, id: int):
        for i in self.__errors:
            if i.get("id") == id:
                print(RED, i.get("desc"), RESET)
                return

        # if the error id doesn't exist
        print(RED, self.__errors[0].get("desc"), RESET)

    def __show_operation(self, op: Operation):
        category = self.manager.get_category(op.category_id)
        print(
            f"сумма: {op.amount} | тип: {op.type} | категория: {category.title} | дата: {op.date} | ID: {op.id} | описание: {op.title}"
        )

    def __show_all_operations(self):
        data: list[Operation] = self.manager.get_all_operations()

        for i in data:
            self.__show_operation(i)

    def __show_operation_by_id(self):
        print("Введите id операции:")
        while True:
            try:
                operation_id = int(self.__prompt())
                self.__show_operation(self.manager.get_operation(operation_id))
                return
            except Exception as e:
                print("Неверный формат ввода")

    def __show_category(self, cat: Category):
        print(f"id: {cat.id} | название: {cat.title}")

    def __show_all_categories(self):
        data: list[Category] = self.manager.get_all_categories()

        for i in data:
            self.__show_category(i)

    def __get_id(self) -> int:
        while True:
            try:
                print("Укажите id:")
                id = int(self.__prompt())
                return id
            except Exception as e:
                print("Неверный формат ввода")

    def __get_operation_data(self, allowNone=True) -> dict:
        op_data = dict()

        while True:
            print("Тип операции (1 - расход | 2 - доход):")
            type = self.__prompt()
            if type == "1":
                op_data["type"] = "расход"
                break
            elif type == "2":
                op_data["type"] = "доход"
                break
            elif type == "":
                op_data["type"] = None
                break
            print("Неверный формат операции")

        while True:
            try:
                print("Категория (id):")
                type = self.__prompt()
                if type == "": 
                    op_data["category_id"] = None
                    break

                op_data["category_id"] = int(type)
                break
            except Exception as e:
                print("Неверный формат ввода")

        print("Заголовок:")
        type = self.__prompt()
        if type == "":
            op_data["title"] = None
        else:
            op_data["title"] = type

        while True:
            try:
                print("Сумма (формат дробных чисел - 100.5)")
                type = self.__prompt()
                if type == "":
                    op_data["amount"] = None
                    break

                op_data["amount"] = float(type)
                break
            except Exception as e:
                print("Неверный формат ввода")

        print("Дата:")
        type = self.__prompt()
        if type == "":
            op_data["date"] = None
        else:
            op_data["date"] = type

        return op_data

    def run(self):
        while True:
            self.__run_menu(self.__main_commands, False, True)

            self.__prompt()
            os.system("cls")

    def add_operation(self):
        data = self.__get_operation_data()

        self.__show_operation(
            self.manager.add_operation(
                data.get("type"),
                data.get("category_id"),
                data.get("title"),
                data.get("amount"),
                data.get("date"),
            )
        )
        print(f"{GREEN}Сохранено{RESET}")

    def edit_operation(self):
        id = self.__get_id()
        old_op = self.manager.get_operation(id)

        print("Нажмите Enter, чтобы пропустить условие")
        new_op = self.__get_operation_data(allowNone=True)
        new_op["id"] = id

        self.__show_operation(self.manager.edit_operation(old_op, new_op))
        print(f"{GREEN}Сохранено{RESET}")

    def remove_operation(self):
        pass

    def show_filtered_operations(self):
        print("Нажмите Enter, чтобы пропустить условие")

        print("Дата формата DD.MM.YYYY | MM.YYYY | YYYY:")
        date = self.__prompt()

        print("Категория:")
        category = self.__prompt()

        print("Тип:")
        type = self.__prompt()

        info = [date, category, type]
        for i in range(len(info)):
            if not info[i].strip():
                info[i] = None

        date, category, type = info

        data = self.manager.filter_operations(date, category, type)
        for i in data:
            self.__show_operation(i)

    def categories_control(self):
        print("Список категорий:")
        self.__show_all_categories()
        print()
        self.__run_menu(self.__category_commands)

    def add_category(self):
        print("Укажите заголовок:")
        title = self.__prompt()

        cat = self.manager.add_category(title)

        self.__show_category(cat)
        print(f"{GREEN}Сохранено{RESET}")

    def edit_category(self):
        id = self.__get_id()

        print("Укажите заголовок:")
        title = self.__prompt()

        cat = self.manager.edit_category(id, title)

        self.__show_category(cat)
        print(f"{GREEN}Сохранено{RESET}")

    def remove_category(self):
        print("remove_category")

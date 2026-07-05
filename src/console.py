
import os
from datetime import date
from category import Category
from format import *
from operation import Operation, OperationUpdate, OperationData, OperationType
from finance_manager import FinanceManager, Balance

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
            {
                "id": 6,
                "desc": "Показать баланс",
                "prefix": None,
                "action": self.show_balance,
            },
            {
                "id": 7,
                "desc": "Показать статистику по категориям",
                "prefix": None,
                "action": self.show_statistics_by_categories,
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

        self.__errors = {
                0: "<UnexpectedError>",
                1: "<CommandNotFoundError>",
                2: "<InvalidInputFormat>",
                3: "<ValueMustBeANumber>",
                4: "<ObjectNotFoundError>"
            }
        
        self.__messages = {
                0: "Сохранено",
                1: "Готово"
            }

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
            except ValueError:
                self.__show_message(self.__errors.get("3"))

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
            self.__show_message(self.__errors.get(1))

    def __show_message(self, text: str, positive=False, description=""):
        
        color = GREEN if positive else RED
        print(color, text, RESET)

        if description != "":
            print(BLUE, description, RESET)

    def __show_operation(self, op: Operation):
        category = self.manager.get_category(op.category_id)
        print(
            f"{op.type} от {op.date} на сумму {op.amount} в категории {category.title} | ID: {op.id} | детали: {op.title}"
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
            except ValueError:
                self.__show_message(self.__errors.get("3"))

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
            except ValueError:
                self.__show_message(self.__errors.get(3))

    def __get_operation_data(self, allowNone=True) -> OperationUpdate | OperationData:
        op_data = self.manager.get_operation_update_template()

        while True:
            print("Тип операции (1 - расход | 2 - доход):")
            value = self.__prompt()
            if value == "":
                if allowNone: break
            else:
                if OperationType.get_type(value) != None:
                    op_data["type"] = OperationType.get_type(value)
                    break

            self.__show_message(self.__errors.get(2))

        while True:
            print("Категория:")
            value = self.__prompt()
            if value == "": 
                if allowNone: break
            elif not self.manager.category_exists_by_title(value):
                print("Такой категории нет. Создать? (1-Y | Enter-изменить)")
                an = self.__prompt()
                if an == "1":
                    op_data["category_id"] = self.manager.add_category(value).id
                    break
                continue
            else:
                op_data["category_id"] = self.manager.get_category_by_title(value).id
                break

            self.__show_message(self.__errors.get(2))

        while True:
            print("Заголовок:")
            value = self.__prompt()

            if value == "":
                if allowNone: break
            else:
                op_data["title"] = value
                break

            self.__show_message(self.__errors.get(2))

        while True:
            try:
                print("Сумма (формат дробных чисел - 100.5)")
                value = self.__prompt()
                if value == "":
                    if allowNone: break
                else:
                    op_data["amount"] = float(value)
                    break

                self.__show_message(self.__errors.get(2))
            except ValueError:
                self.__show_message(self.__errors.get(3))

        while True:
            print("Дата:")
            value = self.__prompt()
            if value == "":
                if allowNone: break
                else:
                    op_data["date"] = str(date.today().strftime("%d.%m.%Y"))
                    break
            else:
                op_data["date"] = value
                break

        return op_data

    def __show_stats(self, cat_id: int, amount: float):
        print(f"{self.manager.get_category(cat_id).title}: {amount}")

    def run(self):
        while True:
            try:
                self.__run_menu(self.__main_commands, False, True)

                self.__prompt()
                print(f"{RESET}")
                os.system("cls")

            except EOFError:
                print(f"{RESET}")
                os.system("cls")
                self.__run_menu(self.__main_commands, False, True)

            except KeyboardInterrupt:
                print(BOLD, "Работа завершена")
                raise SystemExit

    def add_operation(self):
        data: OperationData = self.__get_operation_data(False)

        self.__show_operation(self.manager.add_operation(data))
        self.__show_message(self.__messages[0], True)

    def edit_operation(self):
        id = self.__get_id()

        while self.manager.operation_exists(id) == False:
            self.__show_message(self.__errors[4])
            id = self.__get_id()

        old_op = self.manager.get_operation(id)

        print("Нажмите Enter, чтобы пропустить условие")
        new_op = self.__get_operation_data(allowNone=True)
        new_op["id"] = id

        self.__show_operation(self.manager.edit_operation(old_op, new_op))
        self.__show_message(self.__messages[0], True)

    def remove_operation(self):
        id = self.__get_id()

        while self.manager.operation_exists(id) == False:
            self.__show_message(self.__errors[4])
            id = self.__get_id()

        self.manager.remove_operation(id)
        self.__show_message(self.__messages[1], True) 

    def show_filtered_operations(self):
        print("Нажмите Enter, чтобы пропустить условие")

        print("Дата формата DD.MM.YYYY | MM.YYYY | YYYY:")
        date = self.__prompt()

        print("Категория:")
        category = self.__prompt()

        print("Тип:")
        type_value = self.__prompt()

        info = [date, category, type_value]
        for i in range(len(info)):
            if not info[i].strip():
                info[i] = None

        date, category, value = info

        data = self.manager.filter_operations(date, category, value)
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
        self.__show_message(self.__messages[0], True)

    def edit_category(self):
        id = self.__get_id()

        while self.manager.category_exists(id) == False:
            self.__show_message(self.__errors[4])
            id = self.__get_id()

        print("Укажите заголовок:")
        title = self.__prompt()  

        cat = self.manager.edit_category(id, title)         

        self.__show_category(cat)
        self.__show_message(self.__messages[0], True)

    def remove_category(self):
        id = self.__get_id()

        while self.manager.category_exists(id) == False:
            self.__show_message(self.__errors[4])
            id = self.__get_id()

        linked_operations = self.manager.category_linked(id)
        if linked_operations != 0:
            self.__show_message(f"Выбранная категория связана с несколькими операциями ({linked_operations})", description="Отредактируйте операции для удаления категорий")
            return

        self.manager.remove_category(id)
        self.__show_message(self.__messages[1], True)

    def show_balance(self):
        data = self.manager.get_balance()

        print(f"Доходы: {data["income"]}")
        print(f"Расходы: {data["expenses"]}")

        print(f"{RED}Баланс: {data["balance"]}{RESET}") if data["balance"] < 0 else print(f"{GREEN}Баланс: {data["balance"]}{RESET}")

    def show_statistics_by_categories(self):
        income = self.manager.get_amount_by_categories(OperationType.INCOME)
        print(f"{BOLD}Доходы:{RESET}")
        for cat_id in income:
            self.__show_stats(cat_id, income.get(cat_id))
        print(f"{BOLD}Итого: {self.manager.get_amount_by_op_type(OperationType.INCOME)}{RESET}")

        print()

        expenses = self.manager.get_amount_by_categories(OperationType.EXPENSE)
        print(f"{BOLD}Расходы:{RESET}")
        for cat_id in expenses:
            self.__show_stats(cat_id, expenses.get(cat_id))
        print(f"{BOLD}Итого: {self.manager.get_amount_by_op_type(OperationType.EXPENSE)}{RESET}")

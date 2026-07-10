
import os
from datetime import date
from dataclasses import dataclass
from typing import Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI

from category import Category
from operation import Operation, OperationData, OperationType
from finance_manager import FinanceManager, Balance, SortType
from config import APP_NAME, APP_VERSION, ERRORS, MESSAGES

@dataclass(frozen=True)
class Format:   
    RESET = "\033[0m"

    DEFAULT = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    INVERTED = "\033[7m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

@dataclass(frozen=True)
class MenuItem:
    key: str = ""
    description: str = ""
    action:  Callable[[], None] | str = ""
    prefix: str | None = None

class Console:
    def __init__(self):
        self.__main_commands = [
            MenuItem("-1", "[DEBUG] Show operation by id", self.__show_operation_by_id, "DEBUG"),
            MenuItem("0", "[DEBUG] Show all operations", self.__show_all_operations, "DEBUG"),
            MenuItem("v", "Показать версию", self.__show_app_info),
            MenuItem("1", "Добавить операцию", self.add_operation),
            MenuItem("2", "Редактировать операцию", self.edit_operation),
            MenuItem("3", "Удалить операцию", self.remove_operation),
            MenuItem("4", "Фильтр", self.show_filtered_operations),
            MenuItem("5", "Управление категориями", self.categories_control),
            MenuItem("6", "Показать баланс", self.show_balance),
            MenuItem("7", "Показать статистику по категориям", self.show_statistics_by_categories),
            MenuItem("8", "Показать последние N операций", self.show_last_n_operations),
        ]

        self.__category_commands = [
            MenuItem("1", "Создать", self.add_category),
            MenuItem("2", "Редактировать", self.edit_category),
            MenuItem("3", "Удалить", self.remove_category)
        ]

        self.__sort_commands = [
            MenuItem("1", "По дате", SortType.DATE),
            MenuItem("2", "По сумме", SortType.AMOUNT),
            MenuItem("3", "По категории", SortType.CATEGORY)
        ]

        self.manager = FinanceManager()

    def __prompt(self, prompt_text: str="", default_text: str="", multiline=False) -> str:
        session = PromptSession(multiline=multiline)
        return session.prompt(ANSI(f"{Format.CYAN}{prompt_text}> {Format.RESET}"), default=default_text, prompt_continuation=ANSI(f"{Format.CYAN}>{Format.RESET}"))

    def __input_command(self):
        return self.__prompt()

    def __run_menu(self, commands: list[MenuItem], showWithPrefix=False, clearScreen=False):
        print("Доступные действия:")

        for i in commands:
            if showWithPrefix == True and i.prefix:
                print(f"{i.key}. {i.description}")

            if not i.prefix:
                print(f"{i.key}. {i.description}")

        key_value = self.__input_command()
        if clearScreen:
            os.system("cls")

        command = MenuItem()

        for cmd in commands:
            if cmd.key == key_value:
                command = cmd

        if command != None:
            if command.prefix:
                print(f"[{command.prefix}]")
            command.action()
        else:
            self.__show_message(ERRORS[1])

    def __show_message(self, text: str, positive=False, description=""):
        
        color = Format.GREEN if positive else Format.RED
        print(color, text, Format.RESET)

        if description != "":
            print(Format.BLUE, description, Format.RESET)

    def __show_operation(self, op: Operation):
        category = self.manager.get_category(op.category_id)
        print(
            f"{op.type} от {op.date} на сумму {op.amount} в категории {category.title} | ID: {op.id} | детали: {op.title}"
        )

    def __show_all_operations(self):
        self.__show_operations_list(self.manager.sort_by_date(self.manager.get_all_operations()))

    def __show_operations_list(self, data: list[Operation]):
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
                self.__show_message(ERRORS.get(3))

    def __show_category(self, cat: Category):
        print(f"id: {cat.id} | название: {cat.title}")

    def __show_all_categories(self):
        self.__show_category_list(self.manager.get_all_categories())

    def __show_category_list(self, data: list[Category]):
        for i in data:
            self.__show_category(i)

    def __get_id(self) -> int:
        while True:
            try:
                print("Укажите id:")
                id = int(self.__prompt())
                return id
            except ValueError:
                self.__show_message(ERRORS.get(3))

    def __get_operation_data(self, data: OperationData | None = None) -> OperationData:
        if data is None:
            data = self.manager.get_operation_template()

        print("Тип операции (1 - расход | 2 - доход):")
        while True:   
            if data["type"] == "расход":
                value = self.__prompt(default_text="1")
            elif data["type"] == "доход":
                value = self.__prompt(default_text="2")
            else:
                value = self.__prompt()

            if value != "":
                data["type"] = FinanceManager.require(OperationType.get_type(value))
                break

            self.__show_message(ERRORS.get(2))

        print("Категория:")
        while True:
            value = self.__prompt(default_text=self.manager.get_category(data["category_id"]).title)

            if value != "": 
                if not self.manager.category_exists_by_title(value):
                    print("Такой категории нет. Создать? (1-Y | Enter-изменить)")
                    an = self.__prompt()
                    if an == "1":
                        data["category_id"] = self.manager.add_category(value).id
                        break
                    continue
                else:
                    data["category_id"] = self.manager.get_category_by_title(value).id
                    break

            self.__show_message(ERRORS.get(2))

        print("Заголовок:")
        while True:          
            value = self.__prompt(default_text=data["title"])
            if value != "":
                data["title"] = value
                break

            self.__show_message(ERRORS.get(2))

        print("Сумма (формат дробных чисел - 100.5)")
        while True:
            try:
                value = self.__prompt(default_text=str(data["amount"]))
                if value != "":
                    data["amount"] = float(value)
                    break

                self.__show_message(ERRORS.get(2))
            except ValueError:
                self.__show_message(ERRORS.get(3))

        print("Дата (Enter - текущая):")
        while True:
            value = self.__prompt(default_text=data["date"])
            if value == "":
                data["date"] = str(date.today().strftime("%d.%m.%Y"))
                break

            data["date"] = value
            break

        return data

    def __show_stats(self, cat_id: int, amount: float):
        print(f"{self.manager.get_category(cat_id).title}: {amount}")

    def __show_actions_list(self, actions: list[MenuItem]):
        for i in actions:
            print(f"{i.key}. {i.description}")

    def __show_app_info(self):
        print(f"{Format.CYAN}{Format.BOLD}{APP_NAME}, v{APP_VERSION}{Format.RESET}")

    def run(self):
        self.__show_app_info()
        print(f"{Format.BOLD}==============================={Format.RESET}")

        while True:
            try:
                self.__run_menu(self.__main_commands, False, True)

                self.__prompt()
                print(f"{Format.RESET}")
                os.system("cls")

            except EOFError:
                print(f"{Format.RESET}")
                os.system("cls")

            except KeyboardInterrupt:
                print(f"{Format.BOLD}Работа завершена")
                raise SystemExit

    def add_operation(self):
        data: OperationData = self.__get_operation_data()

        self.__show_operation(self.manager.add_operation(data))
        self.__show_message(MESSAGES[0], True)

    def edit_operation(self):
        id = self.__get_id()

        while self.manager.operation_exists(id) == False:
            self.__show_message(ERRORS[4])
            id = self.__get_id()

        old_op: Operation = self.manager.get_operation(id)

        print("Нажмите Enter, чтобы пропустить условие")
        new_op = self.__get_operation_data(old_op.to_dict())
        new_op["id"] = id

        self.__show_operation(self.manager.edit_operation(old_op, new_op))
        self.__show_message(MESSAGES[0], True)

    def remove_operation(self):
        id = self.__get_id()

        while self.manager.operation_exists(id) == False:
            self.__show_message(ERRORS[4])
            id = self.__get_id()

        self.manager.remove_operation(id)
        self.__show_message(MESSAGES[1], True) 

    def show_filtered_operations(self):
        print("Нажмите Enter, чтобы пропустить условие")

        print("Дата формата DD.MM.YYYY | MM.YYYY | YYYY:")
        date = self.__prompt()

        print("Категория:")
        category = self.__prompt()

        print("Тип операции (1 - расход | 2 - доход):")
        type_value = self.__prompt()

        print("Сортировать:")   
        while True:
            self.__show_actions_list(self.__sort_commands)
            sort_type_id = self.__prompt()
            
            if sort_type_id != "":
                sort_type = FinanceManager.require(SortType.get_type(sort_type_id))
                break

            self.__show_message(ERRORS.get(2))

        info = [date, category, type_value]
        for i in range(len(info)):
            if not info[i].strip():
                info[i] = None

        date, category, type_value = info

        self.__show_operations_list(self.manager.filter_operations(date, category, type_value, sort_type))

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
        self.__show_message(MESSAGES[0], True)

    def edit_category(self):
        id = self.__get_id()

        while self.manager.category_exists(id) == False:
            self.__show_message(ERRORS[4])
            id = self.__get_id()

        print("Укажите заголовок:")
        title = self.__prompt()  

        cat = self.manager.edit_category(id, title)         

        self.__show_category(cat)
        self.__show_message(MESSAGES[0], True)

    def remove_category(self):
        id = self.__get_id()

        while self.manager.category_exists(id) == False:
            self.__show_message(ERRORS[4])
            id = self.__get_id()

        linked_operations = self.manager.category_linked(id)
        if linked_operations != 0:
            self.__show_message(f"Выбранная категория связана с несколькими операциями ({linked_operations})", description="Отредактируйте операции для удаления категорий")
            return

        self.manager.remove_category(id)
        self.__show_message(MESSAGES[1], True)

    def show_balance(self):
        data: Balance = self.manager.get_balance()

        print(f"Доходы: {data["income"]}")
        print(f"Расходы: {data["expenses"]}")

        print(f"{Format.RED}Баланс: {data["balance"]}{Format.RESET}") if data["balance"] < 0 else print(f"{Format.GREEN}Баланс: {data["balance"]}{Format.RESET}")

    def show_statistics_by_categories(self):
        income = self.manager.get_amount_by_categories(OperationType.INCOME)
        print(f"{Format.BOLD}Доходы:{Format.RESET}")
        for cat_id in income:
            self.__show_stats(cat_id, income.get(cat_id))
        print(f"{Format.BOLD}Итого: {self.manager.get_amount_by_op_type(OperationType.INCOME)}{Format.RESET}")

        print()

        expenses = self.manager.get_amount_by_categories(OperationType.EXPENSE)
        print(f"{Format.BOLD}Расходы:{Format.RESET}")
        for cat_id in expenses:
            self.__show_stats(cat_id, expenses.get(cat_id))
        print(f"{Format.BOLD}Итого: {self.manager.get_amount_by_op_type(OperationType.EXPENSE)}{Format.RESET}")

    def show_last_n_operations(self):
        while True:
            try:
                print("Укажите количество операций:")
                n = int(self.__prompt())
                if n > 0:
                    break
                self.__show_message(ERRORS.get(3))
            except ValueError:
                self.__show_message(ERRORS.get(3))

        self.__show_operations_list(self.manager.get_n_operations(n))


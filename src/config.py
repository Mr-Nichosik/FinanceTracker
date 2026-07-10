
from importlib.metadata import metadata

meta = metadata("FinanceTracker")

APP_NAME = meta["Name"]
APP_VERSION = meta["Version"]
APP_AUTHOR = meta["Author"]

ERRORS = {
    0: "<UnexpectedError>",
    1: "<CommandNotFoundError>",
    2: "<InvalidInputFormat>",
    3: "<ValueMustBeANumber>",
    4: "<ObjectNotFoundError>",
}

MESSAGES = {
    0: "Сохранено", 
    1: "Готово"
}
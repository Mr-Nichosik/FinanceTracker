
from importlib.metadata import metadata

meta = metadata("FinanceTracker")

APP_NAME = meta["Name"]
APP_VERSION = meta["Version"]
APP_AUTHOR = meta["Author"]
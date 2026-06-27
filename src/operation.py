
class Operation:
    TYPES = ["add", "remove", "edit"]

    def __init__(self):
        self.TYPE = "add"
        self.id = ""
        self.type = "expense"
        self.category = "food"
        self.title = "Мороженое"
        self.date = "27.06.2026"
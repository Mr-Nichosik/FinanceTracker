
class Operation:
    def __init__(self, id = 0, type="expense", category="general", title="default_title", date="28.06.2026"):
        self.id = id
        self.type: str = type
        self.category: str = category
        self.title: str = title
        self.date: str = date

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type, "category": self.category, "title": self.title, "date": self.date}
    
    @staticmethod
    def from_dict(data: dict) -> Operation:
        return Operation(data.get("type"), data.get("category"), data.get("title"), data.get("date"))
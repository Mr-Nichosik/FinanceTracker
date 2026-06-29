
class Operation:
    def __init__(self, id=0, type="expense", category=-1, title="default_title", amount=100, date="28.06.2026"):
        self.id = id
        self.type: str = type
        self.category_id: int = category
        self.title: str = title
        self.amount: float = amount
        self.date: str = date

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type, "category_id": self.category_id, "title": self.title, "amount": self.amount, "date": self.date}
    
    @staticmethod
    def from_dict(data: dict) -> Operation:
        return Operation(data.get("id"), data.get("type"), data.get("category_id"), data.get("title"), data.get("amount"), data.get("date"))
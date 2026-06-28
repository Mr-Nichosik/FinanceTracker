
class Category:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title}
    
    @staticmethod
    def from_dict(data: dict) -> Category:
        return Category(data.get("id"), data.get("title"))

from dataclasses import dataclass, asdict
from typing import TypedDict

@dataclass
class Category:
    id: int = 0
    title: str = "default_category_title"

    def to_dict(self) -> CategoryData:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: CategoryData) -> Category:
        return Category(**data)
    
class CategoryData(TypedDict):
    id: int
    title: str

from dataclasses import dataclass, fields, asdict
from typing import TypedDict

class OperationData(TypedDict):
    id: int
    type: str
    category_id: int
    title: str
    amount: float
    date: str

class OperationUpdate(TypedDict):
    id: int
    type: str | None
    category_id: int | None
    title: str | None
    amount: float | None
    date: str | None

@dataclass
class Operation:
    id: int = 0
    type: str = "расход"
    category_id: int = 1
    title: str = "default_title"
    amount: float = 0
    date: str = "01.01.1970"

    @staticmethod
    def blank_update(id: int = 0) -> OperationUpdate:
        return {f.name: None for f in fields(Operation) if f.name != "id"} | {"id": id}

    def to_dict(self) -> OperationData:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: OperationData) -> Operation:
        return Operation(**data)
    

OPERATION_FIELDS = {f.name for f in fields(Operation) if f.name != "id"}
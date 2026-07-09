
from __future__ import annotations

from dataclasses import dataclass, fields, asdict
from typing import TypedDict
from enum import StrEnum

class OperationType(StrEnum):
    EXPENSE = "расход"
    INCOME = "доход"

    @staticmethod
    def get_type(id: str | int) -> OperationType | None:
        return {
            "1": OperationType.EXPENSE, 
            "2": OperationType.INCOME, 
            1: OperationType.EXPENSE, 
            2: OperationType.INCOME
        }.get(id)

@dataclass
class Operation:
    id: int = 0
    type: OperationType = ""
    category_id: int = 1
    title: str = ""
    amount: float = 0
    date: str = ""

    @staticmethod
    def get_template() -> OperationData:
        return Operation().to_dict()

    def to_dict(self) -> OperationData:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: OperationData) -> Operation:
        return Operation(**data)

OPERATION_FIELDS: set[str] = {f.name for f in fields(Operation) if f.name != "id"}

class OperationData(TypedDict):
    id: int
    type: str
    category_id: int
    title: str
    amount: float
    date: str
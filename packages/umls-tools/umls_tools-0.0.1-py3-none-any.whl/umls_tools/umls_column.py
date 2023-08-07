from enum import Enum
from typing import Any


class UmlsColumn(Enum):

    def __new__(cls, *args: Any, **kwargs: Any) -> 'UmlsColumn':
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, description: str) -> None:
        self._description = description

    def __str__(self) -> str:
        return self.name

    @property
    def header(self) -> str:
        return self.name

    @property
    def description(self) -> str:
        return self._description

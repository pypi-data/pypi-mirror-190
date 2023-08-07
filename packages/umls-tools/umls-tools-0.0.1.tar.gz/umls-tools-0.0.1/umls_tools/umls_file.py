from enum import Enum
from typing import List, Any

from umls_tools.umls_column import UmlsColumn


class UmlsFile(Enum):

    def __new__(cls, *args: Any, **kwargs: Any) -> 'UmlsFile':
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, description: str, columns: List[UmlsColumn]) -> None:
        self._description = description
        self._columns = columns

    def __str__(self) -> str:
        return self.name

    @property
    def description(self) -> str:
        return self._description

    @property
    def columns(self) -> List[UmlsColumn]:
        return self._columns

    @property
    def headers(self) -> List[str]:
        return [column.header for column in self.columns]

    @property
    def filename(self) -> str:
        raise NotImplementedError

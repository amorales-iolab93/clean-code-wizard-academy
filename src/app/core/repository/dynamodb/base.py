from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Sequence, Set, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class FilterCommand(BaseModel):
    not_exists: Set[str] = set()
    equals: Dict[str, Any] = {}
    not_equals: Dict[str, Any] = {}


EMPTY_LIST: List[str] = []


class ReadOnlyAbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def retrieve(self, partition_value, sort_value) -> T:
        pass

    @abstractmethod
    def search(
        self,
        partition_id: Optional[Sequence[str]],
        content_prefix: Optional[Sequence[str]],
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None,
    ) -> List[T]:
        pass


class AbstractRepository(ReadOnlyAbstractRepository[T], ABC):
    @abstractmethod
    def remove(self) -> bool:
        pass

    @abstractmethod
    def add_or_replace(self, item: T) -> bool:
        pass

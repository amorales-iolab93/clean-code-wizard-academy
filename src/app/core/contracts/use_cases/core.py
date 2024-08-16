from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class WizardRequestReadOnlyImpl(ABC, Generic[T]):
    @abstractmethod
    async def retrieve(self) -> T:
        pass


class WizardRequestWriteImpl(ABC, Generic[T]):
    @abstractmethod
    async def create(self, payload: T) -> None:
        pass

    @abstractmethod
    async def delete(self, params: T) -> None:
        pass

    @abstractmethod
    async def update(self, params: T, payload: T) -> None:
        pass

    @abstractmethod
    async def update_by(self, params: T) -> None:
        pass


class WizardAssignmentImpl(ABC, Generic[T]):
    @abstractmethod
    async def retrieve(self) -> List[T]:
        pass

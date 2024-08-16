from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Sequence, Set, TypeVar, Union
from boto3.dynamodb.conditions import  Attr, ConditionBase
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class FilterCommand(BaseModel):
    """
    A class that encapsulates filter commands for DynamoDB queries.

    This class provides a mechanism to build filter expressions based on specified conditions.
    It includes conditions for attributes that should not exist, attributes that should equal
    specified values, and attributes that should not equal specified values.

    Attributes:
        not_exists (Set[str]): A set of attribute names that should not exist in the items.
        equals (Dict[str, Any]): A dictionary of attribute names and their values that should be equal.
        not_equals (Dict[str, Any]): A dictionary of attribute names and their values that should not be equal.
    """
    not_exists: Set[str] = set()
    equals: Dict[str, Any] = {}
    not_equals: Dict[str, Any] = {}

    def _build_filter_expression(self) -> Optional[ConditionBase]:
        """
        Builds the filter expression for DynamoDB queries based on the conditions
        specified in the FilterCommand.

        Returns:
            Optional[ConditionBase]: The filter expression built from the conditions.
        """
        
        filter_expression: Optional[ConditionBase]  = None
    
        for attr in self.not_exists:
            condition = Attr(attr).not_exists()
            filter_expression = condition if filter_expression is None else filter_expression & condition
        
        for attr, value in self.equals.items():
            condition = Attr(attr).eq(value)
            filter_expression = condition if filter_expression is None else filter_expression & condition
    
        for attr, value in self.not_equals.items():
            condition = Attr(attr).ne(value)
            filter_expression = condition if filter_expression is None else filter_expression & condition
    
        return filter_expression

    def get_filter_expression(self) -> Optional[ConditionBase]:
        """
        Property to get the filter expression for the FilterCommand.

        This property provides a clean interface to access the filter expression
        built from the conditions specified in the `not_exists`, `equals`, and `not_equals` attributes.

        Returns:
            Optional[ConditionBase]: The filter expression built from the conditions, or None if no conditions are specified.

        Example:
            filter_cmd = FilterCommand(
                not_exists={"attribute1"},
                equals={"attribute2": "value2"},
                not_equals={"attribute3": "value3"}
            )
            filter_expr = filter_cmd.filter_expression
        """
        return self._build_filter_expression()



class ReadOnlyRepositoryAsyncImpl(ABC, Generic[T]):
    """
    An abstract class that defines an interface for a read-only repository.

    This class should be inherited, and its abstract methods should be implemented
    by any class that wishes to provide data retrieval and search functionalities.

    Attributes:
        T: A generic type representing the type of object handled by the repository.
    """
    @abstractmethod
    async def retrieve(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
    ) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None
    ) -> List[T]:
        pass

class WriteOnlyRepositoryAsyncImpl(ABC, Generic[T]):
    """
    An abstract class that extends ReadOnlyAbstractRepository to add data modification capabilities.

    This class should be inherited, and its abstract methods should be implemented
    by any class that wishes to provide functionalities for adding, replacing, and removing data.

    Attributes:
        T: A generic type representing the type of object handled by the repository.
    """
    @abstractmethod
    async def remove_by(
        self,
        partition_value: Optional[Sequence[str]], 
        sort_value: Optional[Sequence[str]]
    ) -> bool:
        pass

    @abstractmethod  
    async def add_or_replace(self, item: T) -> bool:
        pass

    @abstractmethod
    async def add_all(self,items:List[T])-> bool:
        pass

    @abstractmethod            
    async def create_table(self)-> None:
        pass
    
class AbstractRepositoryAsyncImpl(WriteOnlyRepositoryAsyncImpl[T],ReadOnlyRepositoryAsyncImpl[T],ABC):
    @abstractmethod
    async def retrieve(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
    ) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None
    ) -> List[T]:
        pass
    
    """
    Write Only Implementations
    """
    @abstractmethod
    async def remove_by(
        self,
        partition_value: Optional[Sequence[str]], 
        sort_value: Optional[Sequence[str]]
    ) -> bool:
        pass

    @abstractmethod  
    async def add_or_replace(self, item: T) -> bool:
        pass

    @abstractmethod
    async def add_all(self,items:List[T])-> bool:
        pass

    @abstractmethod            
    async def create_table(self)-> None:
        pass
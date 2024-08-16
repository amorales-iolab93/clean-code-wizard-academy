from typing import Any, List, Optional, Sequence, Type, Union
import os
import aioboto3
from boto3.dynamodb.conditions import  Key

from .base import  AbstractRepositoryAsyncImpl, FilterCommand, T


class DynamoDbRepositoryAsync(AbstractRepositoryAsyncImpl[T]):
   
    def __init__(
        self,
        *,
        session: aioboto3.Session,
        item_class: Type[T],
        partition_key: str,
        sort_key: Optional[str] = None,
        table_name: Optional[str] = None,
        region_name: Optional[str] = None,
        url_localhost: Optional[str] = None,
        debugger:Optional[bool] = False
    ):
        self._service_name = "dynamodb"
        self._session = session
        self._table_name = table_name
        self._table_name = table_name or os.getenv("AWS_DYNAMODB_TABLE_NAME", "default_table_name")
        self._region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self._partition_key = partition_key
        self._sort_key = sort_key
        self._item_class = item_class
        self._url_localhost = url_localhost
        self._debugger = debugger

    """
    Read Only Implementations
    """
    async def retrieve(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
    ) -> bool:
        async with self._session.resource(            
            service_name=self._service_name,
            endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            response = await table.get_item(
                Key={
                    self._partition_key: self._partition_id(partition_value),
                    self._sort_key: self._sort_id(sort_value),
                }
            )
            db_item = response.get("Item")
            if db_item:
                item = self._item_class(**db_item)
            else:
                item = None
            return item

  
    async def search(
        self,
        partition_value: Union[str, Sequence[str]],
        sort_value: Optional[Union[str, Sequence[str]]] = [],
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None
    ) -> List[T]:
        items = await self._run_query(
            partition_value = partition_value,  
            sort_value = sort_value,
            sort_ascending = sort_ascending,
            limit = limit,
            filters = filters
        )
        return [self._item_class(**item) for item in items]


    """
    Write Only Implementations
    """
    async def remove_by(
        self,
        partition_value: Optional[Sequence[str]], 
        sort_value: Optional[Sequence[str]]
    ) -> bool:
        async with self._session.resource(            
            service_name=self._service_name,
            endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            response = await table.delete_item(
                Key={
                    self._partition_key: self._partition_id(partition_value),
                    self._sort_key: self._sort_id(sort_value),
                }
            )
            status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
            return response
            
    async def add_or_replace(self, item: T) -> bool:
        async with self._session.resource(
            service_name=self._service_name, 
            endpoint_url=self._url_localhost
        ) as dynamodb:
            item_to_put = item.dict(by_alias=True)
            table = await dynamodb.Table(self._table_name)
            response = await table.put_item(Item=item_to_put)
            status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
            return response

    async def add_all(self,items:List[T])-> bool:
        async with self._session.resource(            
            service_name=self._service_name,
            endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            async with table.batch_writer() as batch:
                for item in items:
                    item_to_put = item.model_dump(by_alias=True)
                    await batch.put_item(Item=item_to_put)
                    
    async def create_table(self)-> None:
        async with self._session.resource(            
            service_name=self._service_name,
            endpoint_url=self._url_localhost
        ) as dynamodb:
            attribute_definitions = [
                {'AttributeName': self._partition_key, 'AttributeType': 'S'}
            ]
            if self._sort_key:
                attribute_definitions.append({'AttributeName': self._sort_key, 'AttributeType': 'S'})

            key_schema = [
                 {'AttributeName': self._partition_key, 'KeyType': 'HASH'}
            ]
            if self._sort_key:
                key_schema.append( {'AttributeName': self._sort_key, 'KeyType': 'RANGE'})
            
            await dynamodb.create_table(
                TableName=self._table_name,
                AttributeDefinitions=attribute_definitions,
                KeySchema=key_schema,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
          
    """
    Helpers Implementation
    """
    def _partition_id(self, 
        partition_ids: Optional[Union[str, Sequence[str]]],        
        content_prefix: Optional[str] = '#'
    ) -> str:
        if partition_ids is None:
            partition_ids = []
        if isinstance(partition_ids, str):
            return f"{partition_ids}"
        else:
            return f"{content_prefix.join(partition_ids)}"

    def _sort_id(self, 
        sort_ids: Optional[Union[str, Sequence[str]]],
        content_prefix: Optional[str] = '#'
    ) -> str:
        if sort_ids is None:
            sort_ids = []
        if isinstance(sort_ids, str):
            return f"{sort_ids}"
        else:
            return f"{content_prefix.join(sort_ids)}"
    
    def _build_key_condition_expression(
        self,
        partition_value: Optional[Union[str, Sequence[str]]], 
        sort_value: Optional[Union[str, Sequence[str]]] = []
    ):
        key_condition = None
        partition_query = Key(self._partition_key).eq(self._partition_id(partition_value)) 
        key_condition = partition_query
        if sort_value:
            sort_query = Key(
             self._sort_key
            ).begins_with(self._sort_id(sort_value))
            key_condition = partition_query & sort_query
        
        return key_condition

    def _build_query(
        self,
        key_condition_expression: Key,
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None
    )-> dict[str, Any]:
        query_params = {
            "KeyConditionExpression": key_condition_expression,
            "ScanIndexForward": sort_ascending,
        }
        if limit and "FilterExpression" not in query_params:
            query_params["Limit"] = limit

        if filters:
            query_params["FilterExpression"] = filters.get_filter_expression()

        return query_params

    async def _run_query(
            self,
            partition_value: Optional[Union[str, Sequence[str]]], 
            sort_value: Optional[Union[str, Sequence[str]]] = [],
            sort_ascending: bool = True,
            limit: Optional[int] = None,
            filters: Optional[FilterCommand] = None
        ):
        key_condition_expression = self._build_key_condition_expression(
            partition_value = partition_value,  
            sort_value =  sort_value     
        )
        query = self._build_query(
            key_condition_expression = key_condition_expression,
            sort_ascending = sort_ascending,
            limit = limit,
            filters = filters
        )
        async with self._session.resource(
            service_name=self._service_name, endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            response = await table.query(**query)
            items = response.get("Items", [])
            return items

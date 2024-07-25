from typing import List, Optional, Sequence, Type, Union

import aioboto3
from boto3.dynamodb.conditions import Attr, Key

from .base import EMPTY_LIST, AbstractRepository, FilterCommand, T


class DynamoDbRepositoryAsync(AbstractRepository[T]):
    @classmethod
    def build(
        cls,
        item_class: Type[T],
        table_name: str,
        partition_key,
        sort_key,
        url_localhost: Optional[str] = None,
    ):
        session = aioboto3.Session()
        return cls(
            item_class=item_class,
            table_name=table_name,
            session=session,
            partition_key=partition_key,
            sort_key=sort_key,
            url_localhost=url_localhost,
        )

    def __init__(
        self,
        *,
        item_class: Type[T],
        table_name: str,
        session,
        partition_key,
        sort_key,
        url_localhost: Optional[str] = None,
    ):
        self._table_name = table_name
        self._item_class = item_class
        self._partition_key = partition_key
        self._sort_key = sort_key
        self._session = session
        self._url_localhost = url_localhost

    async def retrieve(
        self, partition_value: Optional[Sequence[str]], sort_value: Optional[Sequence[str]]
    ) -> T:
        async with self._session.resource(
            service_name="dynamodb", endpoint_url=self._url_localhost
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
        partition_value: Optional[Sequence[str]] = EMPTY_LIST,
        sort_value: Optional[Sequence[str]] = EMPTY_LIST,
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None,
    ) -> List[T]:
        key_condition = Key(self._partition_key).eq(self._partition_id(partition_value)) & Key(
            self._sort_key
        ).begins_with(self._sort_id(sort_value))

        items = await self._build_query(
            key_condition_expression=key_condition,
            sort_ascending=sort_ascending,
            limit=limit,
            filters=filters,
        )
        return [self._item_class(**item) for item in items]

    async def add_or_replace(self, item: T) -> bool:
        async with self._session.resource(
            service_name="dynamodb", endpoint_url=self._url_localhost
        ) as dynamodb:
            item_to_put = item.dict(by_alias=True)
            table = await dynamodb.Table(self._table_name)
            response = await table.put_item(Item=item_to_put)
            status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
            return response

    async def remove(
        self, partition_value: Optional[Sequence[str]], sort_value: Optional[Sequence[str]]
    ) -> bool:
        async with self._session.resource(
            service_name="dynamodb", endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            response = await table.delete_item(
                Key={
                    self._partition_key: self._partition_id(partition_value),
                    self._sort_key: self._sort_id(sort_value),
                }
            )
            return response

    def _partition_id(self, partition_ids: Optional[Union[str, Sequence[str]]]) -> str:
        if partition_ids is None:
            partition_ids = EMPTY_LIST
        if isinstance(partition_ids, str):
            return f"{partition_ids}"
        else:
            return f"{'#'.join(partition_ids)}"

    def _sort_id(self, sort_ids: Optional[Union[str, Sequence[str]]]) -> str:
        if sort_ids is None:
            sort_ids = EMPTY_LIST
        if isinstance(sort_ids, str):
            return f"{sort_ids}"
        else:
            return f"{'#'.join(sort_ids)}"

    async def _build_query(
        self,
        key_condition_expression: Key,
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        filters: Optional[FilterCommand] = None,
    ):
        query_params = {
            "KeyConditionExpression": key_condition_expression,
            "ScanIndexForward": sort_ascending,
        }
        if limit and "FilterExpression" not in query_params:
            query_params["Limit"] = limit

        if filters:
            query_params["FilterExpression"] = self._build_filter_expression(filter_command=filters)

        async with self._session.resource(
            service_name="dynamodb", endpoint_url=self._url_localhost
        ) as dynamodb:
            table = await dynamodb.Table(self._table_name)
            response = await table.query(**query_params)
            total_count = response["Count"]
            items = response.get("Items", [])
            return items

    def _build_filter_expression(self, filter_command: FilterCommand):
        filter_expression = None
        for attr in filter_command.not_exists:
            condition = Attr(attr).not_exists()
            filter_expression = (
                condition if filter_expression is None else filter_expression & condition
            )

        for attr, value in filter_command.equals.items():
            condition = Attr(attr).eq(value)
            filter_expression = (
                condition if filter_expression is None else filter_expression & condition
            )

        for attr, value in filter_command.not_equals.items():
            condition = Attr(attr).ne(value)
            filter_expression = (
                condition if filter_expression is None else filter_expression & condition
            )

        return filter_expression

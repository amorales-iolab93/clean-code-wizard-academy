import pytest
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.models.core import AcademyRecordIndex
from app.models.views.view_wizard_request import ViewWizardRequest

from tests import mocks
from unittest.mock import AsyncMock, patch, MagicMock
from faker import Faker

fake = Faker()
TABLE_NAME:str = "wizard-academy-mock"

@pytest.mark.asyncio
@patch("aioboto3.Session")
async def test_dynamo_repo_retrieve(mock_session):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table

    partition_value=["kingdom", "clover_kingdom"]
    sort_value=["wizard","323b5cca-b124-4883-9212-00438cfd78b4" ]
    db_item = mocks.get_db_wizard_request()
    mock_table.get_item.return_value = {"Item": db_item}

    # Act 
    # init repository with mocks an execute artefact
    repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        item_class=ViewWizardRequest,
        table_name=TABLE_NAME,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        session=mock_session
    )

    item = await repository.retrieve(partition_value, sort_value)
    # Assert 
    assert item is not None 
    assert isinstance(item, ViewWizardRequest)
    assert item.pk == "kingdom#clover_kingdom"
    assert item.sk == "wizard#323b5cca-b124-4883-9212-00438cfd78b4"


@pytest.mark.asyncio
@patch("aioboto3.Session")
@pytest.mark.usefixtures("table_items")
async def test_dynamo_repo_search(mock_session,table_items):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}

    partition_value=["kingdom", "clover_kingdom"]
    sort_value=["wizard"]

    # Act 
    # init repository with mocks an execute artefact
    repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        item_class=ViewWizardRequest,
        table_name=TABLE_NAME,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        session=mock_session
    )

    items = await repository.search(partition_value, sort_value)

    # Assert 
    mock_table.query.assert_called_once()
    assert len(items) == len(table_items)
    for item, db_item in zip(items, table_items):
        assert isinstance(item, ViewWizardRequest)
        assert item.pk == db_item[AcademyRecordIndex.PK]
        assert item.sk == db_item[AcademyRecordIndex.SK]
   


@pytest.mark.asyncio
@patch("aioboto3.Session")
async def test_dynamo_repo_add_or_replace(mock_session):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    db_item = ViewWizardRequest(**mocks.get_db_wizard_request())

    # Act 
    # init repository with mocks an execute artefact
    repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        item_class=ViewWizardRequest,
        table_name=TABLE_NAME,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        session=mock_session
    )
    mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    result = await repository.add_or_replace(db_item)

    # Assert 
    mock_table.put_item.assert_called_once_with(Item=db_item.dict(by_alias=True))
    assert result.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200


@pytest.mark.asyncio
@patch("aioboto3.Session")
async def test_dynamo_repo_remove(mock_session):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    partition_value=["kingdom", "clover_kingdom"]
    sort_value=["wizard","323b5cca-b124-4883-9212-00438cfd78b4" ]

    # Act 
    # init repository with mocks an execute artefact
    repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        item_class=ViewWizardRequest,
        table_name=TABLE_NAME,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        session=mock_session
    )
    mock_table.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    result = await repository.remove_by(partition_value, sort_value)

    # Assert 
    mock_table.delete_item.assert_called_once_with(
        Key={
            AcademyRecordIndex.PK: repository._partition_id(partition_value),
            AcademyRecordIndex.SK: repository._sort_id(sort_value),
        }
    )
    assert result.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200
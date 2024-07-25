import os
import pytest
from fastapi.testclient import TestClient
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.models.base import AcademyRecordIndex
from app.models.view.view_wizard_request import ViewWizardRequest
from unittest.mock import AsyncMock, patch
from tests import mocks

#Domain fixtures

TABLE_NAME:str = "wizard-academy-mock"

@pytest.fixture
def table_items():
    return mocks.get_db_wizard_record()
@pytest.fixture
def table_item():
    return mocks.get_db_wizard_request()

@pytest.fixture
@patch("aioboto3.Session")
def mock_repository(mock_session,table_items,table_item):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        item_class=ViewWizardRequest,
        table_name=TABLE_NAME,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        session=mock_session
    )
    mock_table.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_table.get_item.return_value = {"Item": table_item}

    return mock_repository
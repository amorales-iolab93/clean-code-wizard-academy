import os
import pytest
from fastapi.testclient import TestClient
from app.core.config.config import Settings
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.models.core import AcademyRecordIndex
from app.models.request import WizardRequestEntity
from app.models.views.view_wizard_request import ViewWizardRequest
from unittest.mock import AsyncMock, patch
from tests import mocks

@pytest.fixture(autouse=True)
def setup_environment():
    os.environ['ENVIRONMENT_NAME'] = "LOCAL"
    os.environ["AWS_REGION"] = "us-east-1"
    yield


# @pytest.fixture
# @patch("app.core.config.config.Settings")
# def setup_settings(settings,setup_environment):

#     settings.ENVIRONMENT_NAME = "LOCAL"
#     settings.PROJECT_NAME = "Boilerplate"
#     settings.PROJECT_TITLE = "Wizard Academy"
#     settings.PROJECT_DESCRIPTION = "Magic academy system by Jonathan M. Sanchez amorales_lab93@outlook.com"
#     settings.PROJECT_VERSION = "1.0.0"
#     settings.ENCODING = "utf-8"
#     settings.API_V1_PREFIX = "/api/v1"
#     settings.BACKEND_CORS_ORIGINS = ["*"]
#     settings.LOG_LEVEL = "DEBUG"
#     settings.PROJECT_TABLE = "table-name"
#     settings.AWS_REGION = "aws-region"
#     settings.USE_LOCAL_DB = None


  

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
def mock_report_repository(mock_session,table_items,table_item):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_repository = DynamoDbRepositoryAsync[ViewWizardRequest](
        session= mock_session,
        item_class= ViewWizardRequest,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        table_name=TABLE_NAME
    )
    mock_table.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_table.get_item.return_value = {"Item": table_item}

    return mock_repository

@pytest.fixture
@patch("aioboto3.Session")
def mock_request_repository(mock_session,table_items,table_item):
    # Arrange 
    # SetUp Mocks
    mock_dynamodb = AsyncMock()
    mock_table = AsyncMock()
    mock_session.resource.return_value.__aenter__.return_value = mock_dynamodb
    mock_dynamodb.Table.return_value = mock_table
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_repository = DynamoDbRepositoryAsync[WizardRequestEntity](
        session= mock_session,
        item_class= WizardRequestEntity,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        table_name=TABLE_NAME
    )
    mock_table.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mock_table.query.return_value = {"Count": len(table_items), "Items": table_items}
    mock_table.get_item.return_value = {"Item": table_item}

    return mock_repository
from app.core.config.config import get_settings
from app.core.repository.dynamodb.base import AbstractRepositoryAsyncImpl
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.models.core import AcademyRecordIndex
from app.models.request import WizardRequestEntity
from app.models.views.view_wizard_request import ViewWizardRequest
from dependency_injector import containers, providers
import aioboto3

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.models.request",
            "app.services.wizard.report_service"
        ]   
    )

    report_repository = providers.Factory(
        DynamoDbRepositoryAsync[ViewWizardRequest],
        session= aioboto3.Session(),
        item_class= ViewWizardRequest,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        table_name=get_settings().PROJECT_TABLE,
        url_localhost=get_settings().USE_LOCAL_DB,
    )

    request_repository = providers.Factory(
        DynamoDbRepositoryAsync[WizardRequestEntity],
        session= aioboto3.Session(),
        item_class= WizardRequestEntity,
        partition_key=AcademyRecordIndex.PK,
        sort_key=AcademyRecordIndex.SK,
        table_name=get_settings().PROJECT_TABLE,
        url_localhost=get_settings().USE_LOCAL_DB,
    )





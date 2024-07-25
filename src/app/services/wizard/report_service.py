from typing import List

from app.api.v1.assignments.schemas.response import WizardAssignmentsViewModel
from app.api.v1.requests.schemas.response import WizardRequestsViewModel
from app.core.config.config import get_settings
from app.core.repository.dynamodb.base import FilterCommand
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.models.base import AcademyRecordIndex
from app.models.view import view_wizard_request
from app.services.mappers.view_model_mapper import ViewModelMapper


class ReportService:
    def __init__(self):
        db_repository = DynamoDbRepositoryAsync[view_wizard_request.ViewWizardRequest].build(
            item_class=view_wizard_request.ViewWizardRequest,
            table_name=get_settings().PROJECT_TABLE,
            partition_key=AcademyRecordIndex.PK,
            sort_key=AcademyRecordIndex.SK,
            url_localhost=get_settings().USE_LOCAL_DB,
        )
        self._db_repository = db_repository

    async def retrieve_assignments(self, disabled=False) -> List[WizardAssignmentsViewModel]:
        retrieve_assignments = await self._retrieve_list(disabled)
        assignments_view_model = ViewModelMapper.mapper_to_view_assignments(retrieve_assignments)
        return assignments_view_model

    async def retrieve_requests(self, disabled=False) -> WizardRequestsViewModel:
        retrieve_requests = await self._retrieve_list(disabled)
        request_view_model = ViewModelMapper.mapper_to_view_requests(retrieve_requests)
        return request_view_model

    async def _retrieve_list(self, disabled=False) -> List[view_wizard_request.ViewWizardRequest]:
        filter_command = FilterCommand(equals={"Disabled": disabled})
        retrieve_list = await self._db_repository.search(
            partition_value=["kingdom", "clover_kingdom"],
            sort_value="wizard",
            filters=filter_command,
        )
        return retrieve_list

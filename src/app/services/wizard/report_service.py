from typing import List

from fastapi import Depends

from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.api.v1.requests.schemas.response import WizardRequestsSchema
from app.core.containers import Container
from app.core.contracts.services.report_service_interface import ReportServiceInterface

from app.core.repository.dynamodb.base import FilterCommand
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync

from app.models.views import view_wizard_request
from app.services.mappers.view_model_mapper import ViewModelMapper

from dependency_injector.wiring import inject, Provide

class ReportService(ReportServiceInterface):
    @inject
    def __init__(
            self, 
            db_repository:DynamoDbRepositoryAsync[view_wizard_request.ViewWizardRequest]=
            Depends(Provide[Container.report_repository])
            
        ):
        self._db_repository = db_repository

    async def retrieve_assignments(self, disabled=False) -> List[WizardAssignmentsSchema]:
        retrieve_assignments = await self._retrieve_list(disabled)
        assignments_view_model = ViewModelMapper.mapper_to_view_assignments(retrieve_assignments)
        return assignments_view_model

    async def retrieve_requests(self, disabled=False) -> WizardRequestsSchema:
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

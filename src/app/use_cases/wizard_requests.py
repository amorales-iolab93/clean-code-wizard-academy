from fastapi import Depends
from app.api.v1.requests.schemas.request import (
    DeleteParamsRegisterRequestSchema,
    RegisterRequestSchema,
    UpdateParamsRegisterByRequestSchema,
    UpdateParamsRegisterRequestSchema,
    UpdateRegisterRequestSchema,
)
from app.api.v1.requests.schemas.response import WizardRequestsSchema
from app.core.contracts.services.report_service_interface import ReportServiceInterface
from app.core.contracts.services.requests_service_interface import RequestsServiceInterface
from app.core.contracts.use_cases.wizard_requests_interface import WizardRequestsUseCaseInterface
from app.services.wizard.report_service import ReportService
from app.services.wizard.requests_service import RequestsService


class WizardRequestsUseCase(
   WizardRequestsUseCaseInterface
):
    def __init__(
        self,
        report_service: ReportService = Depends(),
        requests_service: RequestsService = Depends(),
    ):
        self._report_service: ReportServiceInterface = report_service
        self._requests_service: RequestsServiceInterface = requests_service

    async def retrieve(self) -> WizardRequestsSchema:
        retrieve_record = await self._report_service.retrieve_requests()
        return retrieve_record

    async def create(self, payload: RegisterRequestSchema) -> None:
        await self._requests_service.create_request(payload)

    async def delete(self, params: DeleteParamsRegisterRequestSchema) -> None:
        await self._requests_service.delete_request(params)

    async def update(
        self, params: UpdateParamsRegisterRequestSchema, payload: UpdateRegisterRequestSchema
    ) -> None:
        await self._requests_service.update_request(params, payload)

    async def update_by(self, params: UpdateParamsRegisterByRequestSchema) -> None:
        await self._requests_service.update_by_request(params)

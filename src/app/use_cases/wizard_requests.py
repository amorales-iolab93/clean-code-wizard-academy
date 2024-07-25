from typing import List

from fastapi import Depends

from app.api.v1.requests.schemas.request import (
    BaseRequest,
    DeleteParamsRegisterRequest,
    RegisterRequest,
    UpdateParamsRegisterByRequest,
    UpdateParamsRegisterRequest,
    UpdateRegisterRequest,
)
from app.api.v1.requests.schemas.response import WizardRequestsViewModel
from app.services.wizard.report_service import ReportService
from app.services.wizard.requests_service import RequestsService
from app.use_cases.core.base import WizardRequestReadOnlyImpl, WizardRequestWriteImpl


class WizardRequestsUseCase(
    WizardRequestReadOnlyImpl[WizardRequestsViewModel], WizardRequestWriteImpl[BaseRequest]
):
    def __init__(
        self,
        report_service: ReportService = Depends(),
        requests_service: RequestsService = Depends(),
    ):
        self._report_service: ReportService = report_service
        self._requests_service: RequestsService = requests_service

    async def retrieve(self) -> WizardRequestsViewModel:
        retrieve_record = await self._report_service.retrieve_requests()
        return retrieve_record

    async def create(self, payload: RegisterRequest) -> None:
        await self._requests_service.create_request(payload)

    async def delete(self, params: DeleteParamsRegisterRequest) -> None:
        await self._requests_service.delete_request(params)

    async def update(
        self, params: UpdateParamsRegisterRequest, payload: UpdateRegisterRequest
    ) -> None:
        await self._requests_service.update_request(params, payload)

    async def update_by(self, params: UpdateParamsRegisterByRequest) -> None:
        await self._requests_service.update_by_request(params)

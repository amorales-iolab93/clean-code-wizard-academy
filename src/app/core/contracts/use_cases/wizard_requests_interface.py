from abc import ABC, abstractmethod
from app.api.v1.requests.schemas.request import (
    BaseRequestSchema,
    DeleteParamsRegisterRequestSchema,
    RegisterRequestSchema,
    UpdateParamsRegisterByRequestSchema,
    UpdateParamsRegisterRequestSchema,
    UpdateRegisterRequestSchema,
)
from app.api.v1.requests.schemas.response import WizardRequestsSchema
from app.core.contracts.use_cases.core import WizardRequestReadOnlyImpl, WizardRequestWriteImpl


class WizardRequestsUseCaseInterface(
    WizardRequestReadOnlyImpl[WizardRequestsSchema], WizardRequestWriteImpl[BaseRequestSchema], ABC
):

    @abstractmethod
    async def retrieve(self) -> WizardRequestsSchema:
        pass
    @abstractmethod
    async def create(self, payload: RegisterRequestSchema) -> None:
        pass
    @abstractmethod
    async def delete(self, params: DeleteParamsRegisterRequestSchema) -> None:
        pass
    @abstractmethod
    async def update(
        self, params: UpdateParamsRegisterRequestSchema, payload: UpdateRegisterRequestSchema
    ) -> None:
        pass
    @abstractmethod
    async def update_by(self, params: UpdateParamsRegisterByRequestSchema) -> None:
        pass

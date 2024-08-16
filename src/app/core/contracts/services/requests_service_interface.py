from abc import ABC, abstractmethod
from app.api.v1.requests.schemas.request import (
    DeleteParamsRegisterRequestSchema,
    RegisterRequestSchema,
    UpdateParamsRegisterByRequestSchema,
    UpdateParamsRegisterRequestSchema,
    UpdateRegisterRequestSchema,
)


class RequestsServiceInterface(ABC):
    @abstractmethod
    async def create_request(self, payload: RegisterRequestSchema) -> None:
        pass

    @abstractmethod
    async def update_request(
        self, params: UpdateParamsRegisterRequestSchema, payload: UpdateRegisterRequestSchema
    ) -> None:
        pass

    @abstractmethod
    async def update_by_request(self, params: UpdateParamsRegisterByRequestSchema) -> None:
        pass

    @abstractmethod
    async def delete_request(self, params: DeleteParamsRegisterRequestSchema) -> None:
        pass

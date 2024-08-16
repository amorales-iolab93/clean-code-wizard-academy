from fastapi import Depends
from app.api.v1.requests.schemas.request import (
    DeleteParamsRegisterRequestSchema,
    RegisterRequestSchema,
    UpdateParamsRegisterByRequestSchema,
    UpdateParamsRegisterRequestSchema,
    UpdateRegisterRequestSchema,
)
from app.core.containers import Container
from app.core.contracts.services.requests_service_interface import RequestsServiceInterface
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.core.schemas.exception import NotFoundException
from app.models import request
from app.models.mappers.entity_mapper import EntityMapper

from dependency_injector.wiring import inject, Provide

class RequestsService(RequestsServiceInterface):
    @inject
    def __init__(
            self,
            db_repository:DynamoDbRepositoryAsync[request.WizardRequestEntity]=
            Depends(Provide[Container.request_repository])
        ):
        self._db_repository = db_repository

    async def create_request(self, payload: RegisterRequestSchema) -> None:
        request_view_model = EntityMapper.mapper_register_to_view_model(payload)
        await self._db_repository.add_or_replace(request_view_model)

    async def update_request(
        self, params: UpdateParamsRegisterRequestSchema, payload: UpdateRegisterRequestSchema
    ) -> None:
        retrieve_record = await self._db_repository.retrieve(
            partition_value=["kingdom", "clover_kingdom"], sort_value=["wizard", params.record_id]
        )
        if not retrieve_record:
            raise NotFoundException()
        request_view_model = EntityMapper.mapper_update_to_view_model(
            params=params, payload=payload, entity=retrieve_record
        )
        await self._db_repository.add_or_replace(request_view_model)

    async def update_by_request(self, params: UpdateParamsRegisterByRequestSchema) -> None:
      
        retrieve_record = await self._db_repository.retrieve(
            partition_value=["kingdom", "clover_kingdom"], sort_value=["wizard", params.record_id]
        )
        if not retrieve_record:
            raise NotFoundException()
        request_view_model = EntityMapper.mapper_update_by_to_view_model(
            params=params, entity=retrieve_record
        )
        await self._db_repository.add_or_replace(request_view_model)

    async def delete_request(self, params: DeleteParamsRegisterRequestSchema) -> None:
        record_removed = await self._db_repository.remove_by(
            partition_value=["kingdom", "clover_kingdom"], sort_value=["wizard", params.record_id]
        )

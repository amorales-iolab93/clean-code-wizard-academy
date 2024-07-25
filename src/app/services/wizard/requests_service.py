from app.api.v1.requests.schemas.request import (
    DeleteParamsRegisterRequest,
    RegisterRequest,
    UpdateParamsRegisterByRequest,
    UpdateParamsRegisterRequest,
    UpdateRegisterRequest,
)
from app.core.config.config import get_settings
from app.core.enum.response_status import ResponseStatus
from app.core.repository.dynamodb.repository import DynamoDbRepositoryAsync
from app.core.schemas.exception import NotFoundException
from app.models import request
from app.models.base import AcademyRecordIndex
from app.models.mappers.entity_mapper import EntityMapper
from uvicorn.main import logger

class RequestsService:
    def __init__(self):
        db_repository = DynamoDbRepositoryAsync[request.WizardRequestEntity].build(
            item_class=request.WizardRequestEntity,
            table_name=get_settings().PROJECT_TABLE,
            partition_key=AcademyRecordIndex.PK,
            sort_key=AcademyRecordIndex.SK,
            url_localhost=get_settings().USE_LOCAL_DB,
        )
        self._db_repository = db_repository

    async def create_request(self, payload: RegisterRequest) -> None:
        request_view_model = EntityMapper.mapper_register_to_view_model(payload)
        await self._db_repository.add_or_replace(request_view_model)

    async def update_request(
        self, params: UpdateParamsRegisterRequest, payload: UpdateRegisterRequest
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

    async def update_by_request(self, params: UpdateParamsRegisterByRequest) -> None:
      
        retrieve_record = await self._db_repository.retrieve(
            partition_value=["kingdom", "clover_kingdom"], sort_value=["wizard", params.record_id]
        )
        if not retrieve_record:
            raise NotFoundException()
        request_view_model = EntityMapper.mapper_update_by_to_view_model(
            params=params, entity=retrieve_record
        )
        await self._db_repository.add_or_replace(request_view_model)

    async def delete_request(self, params: DeleteParamsRegisterRequest) -> None:
        record_removed = await self._db_repository.remove(
            partition_value=["kingdom", "clover_kingdom"], sort_value=["wizard", params.record_id]
        )

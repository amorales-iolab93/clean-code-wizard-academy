from typing import Tuple

from app.api.v1.requests.schemas.request import (
    RegisterRequest,
    UpdateParamsRegisterByRequest,
    UpdateParamsRegisterRequest,
    UpdateRegisterRequest,
)
from app.models import request


class EntityMapper:
    @staticmethod
    def mapper_register_to_view_model(payload: RegisterRequest) -> request.WizardRequestEntity:
        result = request.WizardRequestEntity(
            **{
                "AcademyId": f"kingdom#clover_kingdom",
                "ResourceId": f"wizard#{payload.id}",
                "RequestId": payload.id,
                "Name": payload.name,
                "LastName": payload.last_name,
                "Age": payload.age,
                "MagicSkill": payload.magic_skill,
                "WizardRequestStatus": payload.status,
            }
        )
        return result

    def mapper_update_to_view_model(
        params: UpdateParamsRegisterRequest,
        payload: UpdateRegisterRequest,
        entity: request.WizardRequestEntity,
    ) -> request.WizardRequestEntity:
        result = request.WizardRequestEntity(
            **{
                "AcademyId": f"kingdom#clover_kingdom",
                "ResourceId": f"wizard#{params.record_id}",
                "RequestId": params.record_id,
                "Name": payload.name,
                "LastName": payload.last_name,
                "Age": payload.age,
                "MagicSkill": payload.magic_skill,
                "WizardRequestStatus": entity.status,
                "Grimori": entity.grimorie,
                "CreatedAt": entity.created_at,
            }
        )
        return result

    def mapper_update_by_to_view_model(
        params: UpdateParamsRegisterByRequest, entity: request.WizardRequestEntity
    ) -> request.WizardRequestEntity:
        result = request.WizardRequestEntity(
            **{
                "AcademyId": f"kingdom#clover_kingdom",
                "ResourceId": f"wizard#{params.record_id}",
                "RequestId": params.record_id,
                "Name": entity.name,
                "LastName": entity.last_name,
                "Age": entity.age,
                "MagicSkill": entity.magic_skill,
                "WizardRequestStatus": params.status,
                "Grimori": entity.grimorie,
                "CreatedAt": entity.created_at,
            }
        )
        return result

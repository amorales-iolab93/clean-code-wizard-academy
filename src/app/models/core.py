from abc import ABC
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.core.utils.datetime_utils import DateTimeHelper


class MagicSkillEnum(str, Enum):
    darkness = "Darkness"
    light = "Light"
    fire = "Fire"
    water = "Water"
    wind = "Wind"
    ground = "Ground"


class AcademyRecordIndex(str, Enum):
    PK = "AcademyId"
    SK = "ResourceId"


class AcademyRecord(ABC, BaseModel):
    pk: str = Field(..., alias="AcademyId")
    sk: str = Field(..., alias="ResourceId")
    disabled: Optional[bool] = Field(False, alias="Disabled")
    created_at: int = Field(
        default_factory=lambda: DateTimeHelper.now_timestamp(), alias="CreatedAt"
    )
    updated_at: int = Field(
        default_factory=lambda: DateTimeHelper.now_timestamp(), alias="UpdatedAt"
    )

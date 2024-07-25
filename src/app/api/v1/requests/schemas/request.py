import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.models.base import MagicSkillEnum
from app.models.request import WizardGrimorieTypes, WizardRequestStatus


class BaseRequest(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    record_id: Optional[str] = Field(None, alias="record_id")
    name: Optional[str] = Field(None, alias="name")
    last_name: Optional[str] = Field(None, alias="last_name")
    age: Optional[int] = Field(0, alias="age")
    magic_skill: Optional[MagicSkillEnum] = Field(None, alias="magic_skill")
    status: Optional[WizardRequestStatus] = Field(None, alias="status")
    grimorie: Optional[WizardGrimorieTypes] = Field(None, alias="Grimorie")


class RegisterBaseRequest(BaseRequest):
    name: str = Field(..., alias="name", min_length=1, max_length=20, description="User name")
    last_name: str = Field(
        ..., alias="last_name", min_length=1, max_length=20, description="User last name"
    )
    age: int = Field(..., gt=13, alias="age", description="User age must be greater than 13")
    magic_skill: MagicSkillEnum = Field(..., alias="magic_skill")


class RegisterRequest(RegisterBaseRequest):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), alias="id", description="Unique identifier"
    )
    status: WizardRequestStatus = Field(
        default=WizardRequestStatus.IN_PROCESS, alias="status", description="Request status"
    )


class DeleteParamsRegisterRequest(BaseRequest):
    """
    DeleteParamsRegisterRequest holds record_id to delete request
    Attributes:
        record_id: Request id.
    """
    record_id: str = Field(..., alias="record_id")


class UpdateParamsRegisterRequest(BaseRequest):
    """
    UpdateParamsRegisterRequest holds record_id
    Attributes:
        record_id: Request id.
    """
    record_id: str = Field(..., alias="record_id")


class UpdateRegisterRequest(RegisterBaseRequest):
    """
    UpdateRegisterRequest holds information to update a request 
    Attributes:
        name: Wizard name.
        last_name: Wizard last name.
        age: Wizard age.
        magic_skill: Wizard skills could be Darkness, Light, Fire, Water, Wind or Ground.
    """
    pass


class UpdateParamsRegisterByRequest(BaseRequest):
    """
    UpdateParamsRegisterByRequest holds information to update status of request 
    Attributes:
        record_id: Request id.
        status: Request status could be approved, rejected or in_process.
    """
    record_id: str = Field(..., alias="record_id")
    status: WizardRequestStatus = Field(..., alias="status")

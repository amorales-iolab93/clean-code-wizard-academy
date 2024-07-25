from typing import Optional

from pydantic import Field

from app.models.base import AcademyRecord, MagicSkillEnum
from app.models.request import WizardGrimorieTypes, WizardRequestStatus


class ViewWizardRequest(AcademyRecord):
    request_id: Optional[str] = Field(None, alias="RequestId")
    name: Optional[str] = Field(None, alias="Name")
    last_name: Optional[str] = Field(None, alias="LastName")
    age: Optional[int] = Field(None, alias="Age")
    magic_skill: Optional[MagicSkillEnum] = Field(None, alias="MagicSkill")
    status: Optional[WizardRequestStatus] = Field(
        WizardRequestStatus.IN_PROCESS, alias="WizardRequestStatus"
    )
    grimorie: Optional[WizardGrimorieTypes] = Field(None, alias="Grimorie")

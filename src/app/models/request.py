import random
from enum import Enum
from typing import Any, Optional

from pydantic import Field, root_validator

from app.models.base import AcademyRecord, MagicSkillEnum


class WizardRequestStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROCESS = "in_process"


class WizardGrimorieTypes(str, Enum):
    ONE_LEAF = "one-leaf-clover"
    TWO_LEAF = "two-leaf-clover"
    THREE_LEAF = "three-leaf-clover"
    FOUR_LEAF = "four-leaf-clover"


class WizardRequestEntity(AcademyRecord):
    request_id: str = Field(..., alias="RequestId")
    name: str = Field(..., alias="Name")
    last_name: str = Field(..., alias="LastName")
    age: int = Field(..., alias="Age")
    magic_skill: Optional[MagicSkillEnum] = Field(None, alias="MagicSkill")
    status: Optional[WizardRequestStatus] = Field(
        WizardRequestStatus.IN_PROCESS, alias="WizardRequestStatus"
    )
    grimorie: Optional[WizardGrimorieTypes] = Field(None, alias="Grimorie")

    @root_validator(pre=False)
    def _validate_status(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values["status"] == WizardRequestStatus.APPROVED:
            values["grimorie"] = WizardRequestEntity.get_random_grimorie()
        else:
            values["grimorie"] = None
        return values

    @staticmethod
    def get_random_grimorie(samples: int = 5, special_samples: int = 1):
        random_clover = [1, 2, 3] * samples + [4] * special_samples
        choice = random.choice(random_clover)
        clovers = {
            1: WizardGrimorieTypes.ONE_LEAF,
            2: WizardGrimorieTypes.TWO_LEAF,
            3: WizardGrimorieTypes.THREE_LEAF,
            4: WizardGrimorieTypes.FOUR_LEAF,
        }
        return clovers[choice]

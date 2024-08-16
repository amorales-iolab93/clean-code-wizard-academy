from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.core import MagicSkillEnum
from app.models.request import WizardRequestStatus


class WizardRequestsRecord(BaseModel):
    """
    Model to hold request from wizard academy

    Attributes:
        request_id: Request id.
        name: Wizard name.
        last_name: Wizard last name.
        age: Wizard age.
        magic_skill: Wizard skills could be Darkness, Light, Fire, Water, Wind or Ground.
        status: Request status could be approved, rejected or in_process.
    """
    request_id: Optional[str] = Field(None, alias="request_id")
    name: Optional[str] = Field(None, alias="name")
    last_name: Optional[str] = Field(None, alias="last_name")
    age: Optional[int] = Field(None, alias="age")
    magic_skill: Optional[MagicSkillEnum] = Field(None, alias="magic_skill")
    status: Optional[WizardRequestStatus] = Field(
        WizardRequestStatus.IN_PROCESS, alias="status"
    )


class WizardRequestsSchema(BaseModel):
    """
    WizardRequestsSchema holds information about request 
    of a GET request to /v1/requests

    Attributes:
        size: Assignment size.
        request: List requests.
    """
    size: int = Field(..., alias="size")
    request: Optional[List[WizardRequestsRecord]] = Field([], alias="requests")

    class Config:
        schema_extra = {
            "example":{
                        "size": 3,
                        "requests": [
                            {
                                "request_id": "323b5cca-b124-4883-9212-00438cfd78b1",
                                "name": "Morgana",
                                "last_name": "Le Fay",
                                "age": 25,
                                "magic_skill": "Darkness",
                                "status": "approved"
                            },
                            {
                                "request_id": "323b5cca-b124-4883-9212-00438cfd78b4",
                                "name": "Merlín",
                                "last_name": "Wizard",
                                "age": 30,
                                "magic_skill": "Light",
                                "status": "approved"
                            },
                            {
                                "request_id": "323b5cca-b124-4883-9212-00438cfd78b3",
                                "name": "Rasputín",
                                "last_name": "Wizard",
                                "age": 15,
                                "magic_skill": "Darkness",
                                "status": "approved"
                            }
                        ]
                    }
                    
        }
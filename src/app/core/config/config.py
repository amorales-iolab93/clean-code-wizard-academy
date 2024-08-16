from enum import Enum
from typing import Any, Dict, List, Optional
import os
from pydantic import BaseSettings, validator


class ENVIRONMENT_NAME(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    
class Settings(BaseSettings):
    ENVIRONMENT_NAME: str = os.getenv("ENVIRONMENT_NAME", "LOCAL")
    PROJECT_NAME: str = "Boilerplate"
    PROJECT_TITLE: str = "Wizard Academy"
    PROJECT_DESCRIPTION: str = "Magic academy system by Jonathan M. Sanchez amorales_lab93@outlook.com"
    PROJECT_VERSION: str = "1.0.0"
    ENCODING: str = "utf-8"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    LOG_LEVEL: str = "DEBUG"
    PROJECT_TABLE: str = "table-name"
    AWS_REGION: str = "aws-region"
    USE_LOCAL_DB: Optional[str]= None

    @validator("PROJECT_TABLE", pre=True, always=True)
    def set_table_name(cls, _: Any, values: Dict[str, Any]) -> str:
        match values.get("ENVIRONMENT_NAME"):
            case ENVIRONMENT_NAME.LOCAL:
                return "wizard-academy-local-2"
            case ENVIRONMENT_NAME.DEV:
                return "wizard-academy"
            case _:
                return "wizard-academy"

    @validator("AWS_REGION", pre=True, always=True)
    def set_aws_region(cls, _: Any, values: Dict[str, Any]) -> str:
        match values.get("ENVIRONMENT_NAME"):
            case ENVIRONMENT_NAME.LOCAL:
                return "us-east-1"
            case ENVIRONMENT_NAME.DEV:
                return os.environ["AWS_REGION"]
            case _:
                return os.environ["AWS_REGION"]

    @validator("USE_LOCAL_DB", pre=True, always=True)
    def set_use_local_db(cls, _: Any, values: Dict[str, Any]) -> str:
        match values.get("ENVIRONMENT_NAME"):
            case ENVIRONMENT_NAME.LOCAL:
                return 'http://localhost:8000'
            case ENVIRONMENT_NAME.DEV:
                return None
            case _:
                return None
            
settings = Settings()


def get_settings():
    return Settings()

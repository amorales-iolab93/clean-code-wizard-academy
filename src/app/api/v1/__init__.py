from fastapi import APIRouter

from app.core.config.config import get_settings

from .assignments.controller import assignments_router as assignments_v1_router
from .requests.controller import requests_router as requests_v1_router

settings = get_settings()

router = APIRouter()
router.include_router(
    requests_v1_router, prefix=settings.API_V1_PREFIX + "/requests", tags=["Requests"]
)
router.include_router(
    assignments_v1_router, prefix=settings.API_V1_PREFIX + "/assignments", tags=["Assignments"]
)
__all__ = ["router"]
